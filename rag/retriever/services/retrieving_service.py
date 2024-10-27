from qdrant_client import QdrantClient, models
from retriever.utils import LOGGER
import uuid
import json
import base64
from retriever.config import settings
from retriever.encoders import UserBGEDense, UserBGESparse, BGEReranker
from retriever.schemas import RetrieveResult, TextRetrieveResult, ImageRetrieveResult


class RetrievingService:
    """
    A service for managing and retrieving information from dense, sparse, and image collections
    in Qdrant, with support for re-ranking results based on relevance to a given query.
    """

    def __init__(self):
        """
        Initializes the RetrievingService with collection names, encoders, and a reranker.

        Checks if the required collections are present in Qdrant. If not, it deletes any existing collections
        and creates new ones with the necessary configurations for dense, sparse, and image storage.
        """
        self.client = QdrantClient(host=settings.qdrant.host, port=settings.qdrant.port)
        self.sparse_collection_name = "docs_sparse_collection"
        self.dense_collection_name = "docs_dense_collection"
        self.image_collection_name = "image_collection"
        self.user_bg_sparse = UserBGESparse()
        self.user_bg_dense = UserBGEDense()
        self.reranker = BGEReranker()

        self.check_collections()

    def check_collections(self) -> None:
        """
        Verifies the existence of sparse, dense, and image collections in Qdrant.

        Logs the current collections. If any required collections are missing, it deletes
        all existing collections and calls `_create_and_fill_collections` to create and populate them.
        """
        collections = self.client.get_collections()
        collections_names = [c.name for c in collections.collections]
        LOGGER.info(f"Collections: {collections_names}")
        if (
            self.sparse_collection_name in collections_names
            and self.dense_collection_name in collections_names
            and self.image_collection_name in collections_names
        ):
            LOGGER.info(f"Collections exists: {collections}")
            return
        else:
            LOGGER.info(f"Collections not found, deleting: {collections}")
            for name in collections_names:
                self.client.delete_collection(collection_name=name)
            self._create_and_fill_collections()
            return

    def _create_and_fill_collections(self):
        """
        Creates and populates the dense, sparse, and image collections with text and image data.

        - Creates the dense collection for text embeddings.
        - Processes and uploads text data for dense embedding storage.
        - Creates the sparse collection for sparse vector storage and uploads sparse vector data.
        - Creates the image collection, generates embeddings for images with captions, and uploads them.
        """
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
        data = json.load(open(caption_data_path, "r", encoding="utf-8"))

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
        """
        Retrieves and ranks the nearest text and image results to a given query.

        This method first encodes the query using dense and sparse encoders, retrieves matching text passages
        and images, reranks the results, and returns the top results for each.

        :param query: The query string for which nearest points are to be found.
        :param top_k: The number of top-ranked text results to return.
        :param top_img_k: The number of top-ranked image results to return.

        :returns: A `RetrieveResult` object containing ranked text and image results.
        """
        dense_query = self.user_bg_dense.encode(query, mode="avg-pooling")
        sparse_query = self.user_bg_sparse.encode(query)

        dense_results = self.client.search(
            collection_name=self.dense_collection_name,
            query_vector=dense_query,
            limit=top_k * 3,
        )

        sparse_results = self.client.query_points(
            collection_name=self.sparse_collection_name,
            query=models.SparseVector(
                indices=sparse_query[0][0], values=sparse_query[0][1]
            ),
            using="text",
            limit=top_k * 3,
        )

        # Combine result
        text_chunks = set()
        for dense_result in dense_results:
            text_chunks.add(dense_result.payload["text"])
        for sparse_result in sparse_results.points:
            text_chunks.add(sparse_result.payload["text"])

        # Rerank text passages
        ranked_results = self.reranker.rerank(query, text_chunks, top_k)

        # Find relevant images
        image_results = self.client.search(
            collection_name=self.image_collection_name,
            query_vector=dense_query,
            limit=int(top_img_k * 2),
        )

        # Preprocess and rerank
        image_search_results = set(
            [
                (image_result.payload["img"], image_result.payload["caption"])
                for image_result in image_results
            ]
        )

        image_results = self.reranker.rerank(query, image_search_results, top_img_k)
        # Create results
        text_results = [
            TextRetrieveResult(score=score, passage=text)
            for score, text in ranked_results
        ]

        processed_image_results = []
        for image_result in image_results:
            score = image_result[0]
            img, caption = image_result[1]
            processed_image_results.append(
                ImageRetrieveResult(score=score, b64_image=img, caption=caption)
            )

        return RetrieveResult(
            text_results=text_results, image_results=processed_image_results
        )


retrieving_service = RetrievingService()
