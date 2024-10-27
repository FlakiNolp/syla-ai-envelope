from abc import ABC, abstractmethod

import torch
from FlagEmbedding import FlagReranker
from retriever.config import settings


class CrossEncoder(ABC):
    @abstractmethod
    def rerank(self, query: str, points: list[str], top_k: int) -> tuple[float, str]:
        raise NotImplementedError


class BGEReranker(CrossEncoder):
    """A class to rerank search results based on relevance to a given query using a cross-encoder model."""

    def __init__(self):
        """
        Initializes a BGEReranker instance with a pre-configured `FlagReranker`.

        The reranker model is loaded in evaluation mode and configured to use
        16-bit floating-point precision for improved efficiency.
        """
        self.reranker = FlagReranker(
            settings.reranker.name,
            use_fp16=True,
            device="cuda" if torch.cuda.is_available() else "cpu",
        )
        self.reranker.model.eval()

    def warmup(self):
        """
        Placeholder method for any required warmup operations.

        Currently, this method does not perform any operations but can be
        overridden if initialization logic is needed.
        """
        pass

    def rerank(
        self,
        query: str,
        search_results: list[str] | list[tuple[str, str]],
        top_k: int = 5,
    ) -> list[tuple[float, str]]:
        """
        Reranks the given search results by their relevance to the specified query.
        Each search result is evaluated for its relevance score with respect to the
        provided query. The results are sorted by score in descending order, and the
        top results are returned based on the specified `top_k` value.

        :param query: The search query string to which results are to be reranked.
        :param search_results: A list of search results, where each result can be a
            string or a tuple containing additional information.
        :param top_k: The maximum number of top results to return, default is 5.

        :returns: A list of tuples containing relevance scores and search results,
            sorted in descending order by score.
        """
        scored_results = []
        for result in search_results:
            if isinstance(result, tuple):
                passage = result[1]
            else:
                passage = result
            rerank_score = self.reranker.compute_score(
                (query, passage), normalize=True
            )[0]
            scored_results.append((rerank_score, result))
        scored_results = sorted(scored_results, key=lambda x: x[0], reverse=True)[
            :top_k
        ]
        return scored_results
