from pydantic_settings import BaseSettings
from pydantic import Field


class QdrantConfig(BaseSettings):
    host: str = Field(alias="QDRANT_HOST")
    port: str = Field(alias="QDRANT_PORT")


class DenseRetrieverConfig(BaseSettings):
    name: str = Field(alias="DENSE_RETRIEVER_NAME", default="deepvk/USER-bge-m3")


class SparseRetrieverConfig(BaseSettings):
    name: str = Field(alias="SPARSE_RETRIEVER_NAME", default="deepvk/USER-bge-m3")


class RerankerConfig(BaseSettings):
    name: str = Field(alias="RERANKER_NAME", default="BAAI/bge-reranker-v2-gemma")


class Config(BaseSettings):
    qdrant: QdrantConfig = QdrantConfig()
    dense_retriever: DenseRetrieverConfig = DenseRetrieverConfig()
    sparse_retriever: SparseRetrieverConfig = SparseRetrieverConfig()
    reranker: RerankerConfig = RerankerConfig()


settings = Config()
