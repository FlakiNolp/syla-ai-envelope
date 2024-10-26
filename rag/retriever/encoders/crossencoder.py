from abc import ABC, abstractmethod
from FlagEmbedding import FlagReranker
from retriever.config import settings


class CrossEncoder(ABC):
    @abstractmethod
    def rerank(self, query: str, points: list[str], top_k: int) -> tuple[float, str]:
        raise NotImplementedError


class BGEReranker(CrossEncoder):
    def __init__(self):
        self.reranker = FlagReranker(settings.reranker.name, use_fp16=True)
        self.reranker.model.eval()

    def warmup(self):
        pass

    def rerank(
        self,
        query: str,
        search_results: list[str] | list[tuple[str, str]],
        top_k: int = 5,
    ) -> list[tuple[float, str]]:
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
