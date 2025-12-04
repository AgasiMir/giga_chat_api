from fastapi import APIRouter, Depends, Request, status

from src.database.db_depends import get_session
from src.giga_chat_client import get_giga_response
from src.repository.crud import add_request_data, get_user_requests
from src.schemas import CreatePromtSchema, PromtSchema

router = APIRouter(prefix="/requests", tags=["requests ❔❓"])


@router.get("/", response_model=list[PromtSchema])
async def get_my_requests(request: Request, session=Depends(get_session)):
    # Проверяем, что request.client не None перед доступом к host
    if request.client is not None:
        user_ip_address = request.client.host
    else:
        # Если клиент недоступен, используем заголовок X-Forwarded-For или значение по умолчанию
        user_ip_address = request.headers.get("X-Forwarded-For", "unknown")

    user_requests = await get_user_requests(ip_address=user_ip_address, session=session)
    return user_requests


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_my_request(prompt: CreatePromtSchema, request: Request, session=Depends(get_session)):
    # Проверяем, что request.client не None перед доступом к host
    if request.client is not None:
        user_ip_address = request.client.host
    else:
        # Если клиент недоступен, используем заголовок X-Forwarded-For или значение по умолчанию
        user_ip_address = request.headers.get("X-Forwarded-For", "unknown")
    answer = get_giga_response(prompt.prompt)
    answer = "".join(list(answer)[-1])
    request_data = {
        "ip_address": user_ip_address,
        "prompt": prompt.prompt,
        "response": answer,
    }
    await add_request_data(data=request_data, session=session)
    return {"message": "Request created successfully"}
