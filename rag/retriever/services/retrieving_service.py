from qdrant_client import QdrantClient, models
from retriever.utils import LOGGER
import uuid
import json
import base64
from retriever.config import settings
from retriever.encoders import UserBGEDense, UserBGESparse, BGEReranker
from retriever.schemas import RetrieveResult, TextRetrieveResult, ImageRetrieveResult


class RetrievingService:
    def __init__(self):
        self.client = QdrantClient(host=settings.qdrant.host, port=settings.qdrant.port)
        self.sparse_collection_name = "docs_sparse_collection"
        self.dense_collection_name = "docs_dense_collection"
        self.image_collection_name = "image_collection"
        self.user_bg_sparse = UserBGESparse()
        self.user_bg_dense = UserBGEDense()
        self.reranker = BGEReranker()

        self.check_collections()

    def check_collections(self) -> None:
        collections = self.client.get_collections()
        LOGGER.info(f"Collections: {collections}")
        if (
            self.sparse_collection_name in collections
            and self.dense_collection_name in collections
            and self.image_collection_name in collections
        ):
            LOGGER.info(f"Collections exists: {collections}")
            return
        else:
            LOGGER.info(f"Collections not found, deleting: {collections}")
            for collection in collections:
                self.client.delete_collection(collection_name=collection)
            self._create_and_fill_collections()
            return

    def _create_and_fill_collections(self):
        # Create dense collection
        self.client.create_collection(
            collection_name=self.dense_collection_name,
            vectors_config=models.VectorParams(
                size=1024, distance=models.Distance.COSINE
            ),
        )

        # Prepare late chunks
        text_data_path = settings.base_dir_path / "data/updated_main_text.txt"
        text_data = text_data_path.read_text()
        dense_late_chunks = self.user_bg_dense.create_late_chunks(text_data)

        # And upload
        for chunk in dense_late_chunks:
            for text, embedding in chunk.items():
                self.client.upsert(
                    collection_name=self.dense_collection_name,
                    points=[
                        models.PointStruct(
                            id=uuid.uuid4().hex,
                            payload={"text": text},
                            vector=embedding,
                        )
                    ],
                )

        # Create sparse collection
        self.client.create_collection(
            collection_name=self.sparse_collection_name,
            vectors_config={},
            sparse_vectors_config={
                "text": models.SparseVectorParams(
                    modifier=models.Modifier.IDF,
                )
            },
        )

        # Prepare late chunks
        sparse_vectors = self.user_bg_sparse.encode_text_with_sparse_vectors(text_data)

        # And upload
        for k, v in sparse_vectors.items():
            for vector in v:
                self.client.upsert(
                    collection_name=self.sparse_collection_name,
                    points=[
                        models.PointStruct(
                            id=uuid.uuid4().hex,
                            payload={"text": k},
                            vector={
                                "text": models.SparseVector(
                                    indices=vector[0], values=vector[1]
                                )
                            },
                        )
                    ],
                )

        # Create image collection
        self.client.create_collection(
            collection_name=self.image_collection_name,
            vectors_config=models.VectorParams(
                size=1024, distance=models.Distance.COSINE
            ),
        )

        # Get caption data
        caption_data_path = settings.base_dir_path / "data" / "New document 4.json"
        data = json.load(open(caption_data_path, "r"))

        # And upload
        base_image_dir_path = settings.base_dir_path / "data" / "images_word"
        for name, caption in data.items():
            caption_embedding = self.user_bg_dense.encode(caption, mode="cls-pooling")
            base64_img = base64.b64encode(
                open(base_image_dir_path / f"Рисунок{name}.png", "rb").read()
            )
            self.client.upsert(
                collection_name=self.image_collection_name,
                points=[
                    models.PointStruct(
                        id=uuid.uuid4().hex,
                        payload={"img": base64_img, "caption": caption},
                        vector=caption_embedding,
                    )
                ],
            )
        LOGGER.info("Collections created")

    def get_nearest_points(
        self, query: str, top_k: int, top_img_k: int
    ) -> RetrieveResult:
        dense_query = self.user_bg_dense.encode(query, mode="avg-pooling")
        sparse_query = self.user_bg_sparse.encode_text_with_sparse_vectors(query)

        dense_results = self.client.search(
            collection_name=self.dense_collection_name,
            query_vector=dense_query,
            limit=top_k * 2,
        )

        sparse_results = self.client.query_points(
            collection_name="test_collection_sparse",
            query=models.SparseVector(
                indices=sparse_query[0][0], values=sparse_query[0][1]
            ),
            using="text",
            limit=top_k * 2,
        )

        # Combine result
        text_chunks = []
        for dense_result in dense_results:
            text_chunks.append(dense_result.payload["text"])
        for sparse_result in sparse_results:
            text_chunks.append(sparse_result.payload["text"])

        # Rerank text passages
        ranked_results = self.reranker.rerank(query, text_chunks, top_k)

        # Find relevant images
        image_results = self.client.search(
            collection_name=self.image_collection_name,
            query_vector=dense_query,
            limit=int(top_img_k * 1.5),
        )

        # Preprocess and rerank
        image_search_results = [
            (image_result.payload["img"], image_result.payload["caption"])
            for image_result in image_results
        ]

        image_results = self.reranker.rerank(query, image_search_results, top_img_k)

        text_results = [
            TextRetrieveResult(score=score, passage=text)
            for score, text in ranked_results
        ]
        image_results = [
            ImageRetrieveResult(score=score, b64_image=img, caption=caption)
            for score, img, caption in image_results
        ]
        return RetrieveResult(text_results=text_results, image_results=image_results)


retrieving_service = RetrievingService()
