from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class QdrantConfig(BaseSettings):
    host: str = Field(alias="QDRANT_HOST", default="31.129.50.189")
    port: str = Field(
        alias="QDRANT_PORT",
        default="6333",
    )


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
    base_dir_path: Path = Path(__file__).parent


settings = Config()
