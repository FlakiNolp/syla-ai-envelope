from pydantic import BaseModel


class QARequest(BaseModel):
    query: str


class QAResponse(BaseModel):
    answer: str
    pics: list[str]
