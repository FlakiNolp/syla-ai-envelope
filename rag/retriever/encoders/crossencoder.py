from abc import ABC, abstractmethod
from FlagEmbedding import FlagReranker
from retriever.config import settings


class CrossEncoder(ABC):
    @abstractmethod
    def rerank(self, query: str, points: list[str], top_k: int) -> tuple[float, str]:
        raise NotImplementedError


class BGEM3CrossEncoder(CrossEncoder):
    def __init__(self):
        self.reranker = FlagReranker(settings.reranker.name, use_fp16=True)
        self.reranker.model.eval()

    def warmup(self):
        pass

    def rerank(
        self, query: str, search_results: list[str], top_k: int = 5
    ) -> list[tuple[list[float], str]]:
        scored_results = []
        for result in search_results:
            rerank_score = self.reranker.compute_score((query, result), normalize=True)
            scored_results.append((rerank_score, result))
        scored_results = sorted(scored_results, key=lambda x: x[0], reverse=True)[
            :top_k
        ]
        return scored_results
