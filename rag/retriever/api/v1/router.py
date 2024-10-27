from typing import Annotated
from retriever.services import retrieving_service
from fastapi import APIRouter, Body
from retriever.schemas import RetrieveResult

router = APIRouter(prefix="/v1")


@router.post("/qa/retrieval", response_model=RetrieveResult)
def find_passages(
    query: Annotated[str, Body(embed=True)],
    top_k: Annotated[int, Body(embed=True)],
    top_k_img: Annotated[int, Body(embed=True)],
) -> RetrieveResult:
    return retrieving_service.get_nearest_points(query, top_k, top_k_img)
