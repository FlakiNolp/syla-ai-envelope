from abc import ABC, abstractmethod
from retriever.config import settings
import numpy as np
from torch import nn
import torch
from FlagEmbedding import BGEM3FlagModel
from .utils import safe_text_slice
from transformers import AutoModel, AutoTokenizer


class DenseBiEncoder(ABC):
    @abstractmethod
    def encode(self, query: str, mode: str) -> tuple[str, str]:
        pass

    @abstractmethod
    def create_late_chunks(
        self,
        texts: list[str] | str,
        model_len: int,
        chunk_len: int,
        overlap: int,
    ) -> list[dict[str, np.ndarray]]:
        pass


class SparseBiEncoder(ABC):
    @abstractmethod
    def encode(self, texts: str | list[str]) -> list[tuple[int, float]]:
        pass

    @abstractmethod
    def encode_text_with_sparse_vectors(
        self,
        texts: str | list[str],
        parent_chunk_size: int,
        child_chunk_size: int,
        parent_overlap: int,
        child_overlap: int,
    ) -> np.ndarray:
        pass


class UserBGESparse(SparseBiEncoder):
    """A bi-encoder model for sparse representation of text using the BGEM3FlagModel."""

    def __init__(self):
        """
        Initializes the UserBGESparse bi-encoder model with sparse vector capabilities.
        Loads model weights from a pre-trained state and prepares the sorted vocabulary.
        """
        self.model = BGEM3FlagModel(
            settings.sparse_retriever.name, use_fp16=True, normalize_embeddings=True
        )
        self.model.model.sparse_linear.load_state_dict(
            torch.load(settings.base_dir_path / "encoders" / "sparse_linear.pt")
        )
        self.model.model.eval()

        vocab = self.model.model.tokenizer.get_vocab()
        self.sorted_vocab = {
            k: v for k, v in sorted(vocab.items(), key=lambda item: item[1])
        }

    # TODO: add warmup and torch compile
    def warmup(self):
        raise NotImplementedError

    def encode(
        self, texts: str | list[str]
    ) -> list[tuple[list[int], list[np.float64]]]:
        """
        Encodes text(s) into sparse vectors using the specified vocabulary.

        :param texts: The input text(s) to encode.
        :returns: A list of tuples where each tuple contains:
                  - a list of token indices in the vocabulary.
                  - a list of corresponding lexical weights.t64]]]
        """
        result = self.model.encode(
            texts, return_sparse=True, return_dense=False, return_colbert_vecs=False
        )
        if not isinstance(texts, list):
            result["lexical_weights"] = [result["lexical_weights"]]

        sparse_vectors = []
        for weighted_text in result["lexical_weights"]:
            sparse_vector = [
                weighted_text.get(str(id), 0) for token, id in self.sorted_vocab.items()
            ]
            ind = []
            value = []
            for i, weight in enumerate(sparse_vector):
                if weight != 0:
                    ind.append(i)
                    value.append(weight)
            sparse_vectors.append((ind, value))
        return sparse_vectors

    def encode_text_with_sparse_vectors(
        self,
        texts: str | list[str],
        parent_chunk_size: int = 2000,
        child_chunk_size: int = 512,
        parent_overlap: int = 250,
        child_overlap: int = 100,
    ) -> dict[str | list[str], list[tuple[list[int], list[float]]]]:
        """
        Encodes text(s) by dividing them into hierarchical chunks with specified overlap.

        :param texts: The input text(s) to encode.
        :param parent_chunk_size: The maximum number of tokens in a parent chunk. Default is 2000.
        :param child_chunk_size: The maximum number of tokens in a child chunk. Default is 512.
        :param child_overlap: The overlap between consecutive child chunks. Default is 100.
        :returns: A dictionary with parent chunks as keys and lists of sparse vector tuples for child chunks as values.
        """
        if isinstance(texts, str):
            texts = [texts]

        chunks = {}
        for text in texts:
            parent_chunks = [
                safe_text_slice(text, start, parent_chunk_size, mode="words")[0]
                for start in range(0, len(text), parent_chunk_size - parent_overlap)
            ]
            for parent_chunk in parent_chunks:
                child_chunks = [
                    safe_text_slice(
                        parent_chunk, start, child_chunk_size, mode="words"
                    )[0]
                    for start in range(
                        0, len(parent_chunk), child_chunk_size - child_overlap
                    )
                ]
                sparse_vectors = self.encode(child_chunks)
                chunks[parent_chunk] = sparse_vectors
                # print(child_chunks, sparse_vectors)
        return chunks


class UserBGEDense(DenseBiEncoder):
    """A bi-encoder model for dense representation of text using a pre-trained model from Hugging Face."""

    def __init__(self):
        """
        Initializes the UserBGEDense bi-encoder model for dense vector representation.
        Loads the model and tokenizer from a pre-trained Hugging Face model.
        """
        self.model = AutoModel.from_pretrained(settings.dense_retriever.name)
        self.tokenizer = AutoTokenizer.from_pretrained(settings.dense_retriever.name)

        self.model.eval()

    # TODO: add warmup and torch compile
    def warmup(self):
        raise NotImplementedError

    def create_late_chunks(
        self,
        texts: list[str] | str,
        model_len: int = 8000,
        chunk_len: int = 512,
        overlap: int = 150,
    ) -> list[dict[str, np.ndarray]]:
        """
        Generates embeddings for late chunks of text by splitting and processing in hierarchical chunks.

        :param texts: The input text(s) to be split into chunks and encoded.
        :param model_len: The maximum length of the parent chunk in tokens. Default is 8000.
        :param chunk_len: The maximum length of each smaller child chunk. Default is 512.
        :param overlap: The overlap between consecutive child chunks. Default is 150.
        :returns: A list of dictionaries where each dictionary contains the text chunks as keys
                  and the corresponding dense embeddings as values.
        """
        if isinstance(texts, str):
            texts = [texts]

        texts_embeddings = []
        for text in texts:
            late_chunks = {}
            tokenized_text = self.tokenizer.tokenize(text, add_special_tokens=False)
            for parent_chunk_ind in range(0, len(tokenized_text), model_len):
                tokenized_parent_chunk, _, _ = safe_text_slice(
                    text=tokenized_text,
                    start=parent_chunk_ind,
                    length=model_len,
                    mode="tokens",
                )
                parent_chunk = self.tokenizer.convert_tokens_to_string(
                    tokenized_parent_chunk
                )

                tokenized_parent_chunk = self.tokenizer(
                    parent_chunk, padding=True, truncation=True, return_tensors="pt"
                )
                hidden_states = self.model(**tokenized_parent_chunk).last_hidden_state
                hidden_states = hidden_states[:, 1:-1, :]  # Remove special tokens

                tokenized_parent_chunk = self.tokenizer.convert_ids_to_tokens(
                    tokenized_parent_chunk["input_ids"].squeeze().tolist(),
                    skip_special_tokens=True,
                )

                for chunk_ind in range(
                    0, len(tokenized_parent_chunk), chunk_len - overlap
                ):
                    tokenized_chunk, start, stop = safe_text_slice(
                        text=tokenized_parent_chunk,
                        start=chunk_ind,
                        length=chunk_len,
                        mode="tokens",
                    )
                    chunk_embedding = nn.functional.tanh(
                        hidden_states[:, start:stop, :].mean(dim=1)
                    )
                    # chunk_embedding = nn.functional.tanh(model.pooler.dense(chunk_embedding)).squeeze().detach().numpy()
                    chunk_embedding = chunk_embedding.squeeze().detach().numpy()
                    late_chunks[
                        self.tokenizer.convert_tokens_to_string(tokenized_chunk)
                    ] = chunk_embedding
            texts_embeddings.append(late_chunks)
        return texts_embeddings

    def encode(self, query: str, mode: str) -> np.ndarray[float]:
        """0
        Encodes a single query string into a dense vector representation.

        :param mode: The mode of encoding. Can be 'avg-pooling' or 'cls-pooling'.
        :param query: The query string to be encoded.
        :returns: The dense embedding of the query.
        """
        tokenized_query = self.tokenizer(query, padding=True, truncation=True)
        if mode == "avg-pooling":
            query_embedding = nn.functional.tanh(
                self.model(**tokenized_query).last_hidden_state[:, 1:-1, :].mean(dim=1)
            )
            query_embedding = query_embedding.squeeze().detach().numpy()
        elif mode == "cls-pooling":
            query_embedding = (
                self.model(**tokenized_query)["pooler_output"]
                .squeeze()
                .detach()
                .numpy()
            )
        else:
            raise NotImplementedError
        return query_embedding
