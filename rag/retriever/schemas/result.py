from pydantic import BaseModel


class TextRetrieveResult(BaseModel):
    score: float
    passage: str


class ImageRetrieveResult(BaseModel):
    score: float
    b64_image: str
    caption: str


class RetrieveResult(BaseModel):
    text_results: list[TextRetrieveResult]
    image_results: list[ImageRetrieveResult]
