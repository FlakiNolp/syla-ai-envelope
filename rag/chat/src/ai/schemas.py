from pydantic import BaseModel


class QARequest(BaseModel):
    query: str
    top_k: int = 2
    top_k_img: int = 2


class QAResponse(BaseModel):
    answer: str
    pics: list[str]


class RetrievedContext(BaseModel):
    text: str
    pics: list[str]
