from fastapi import APIRouter

from ai.schemas import QARequest
from ai.utils import generate_answer

router = APIRouter(prefix="/qa")


@router.post("/answer")
async def answer(qa_request: QARequest):
    return await generate_answer(qa_request.query)
