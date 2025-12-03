from fastapi import APIRouter, Depends, status

from src.gemini_client import get_answer_from_gemini
from src.schemas import CreatePromtSchema, PromtSchema

router = APIRouter(prefix="/requests", tags=["requests ❔❓"])


@router.get("/", response_model=list[PromtSchema])
async def get_my_requests():
    return {"Hello": "World"}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_my_request(promt: CreatePromtSchema):
    answer = get_answer_from_gemini(promt.promt)
    return {"answer": answer}
