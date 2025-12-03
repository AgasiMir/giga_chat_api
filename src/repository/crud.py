from typing import Sequence
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.requests_model import Request
from src.schemas import CheckRequestSchema


async def get_user_requests(ip_address: str, session: AsyncSession) -> Sequence[Request]:
    result = await session.scalars(
        select(Request).where(Request.ip_address == ip_address)
    )
    return result.all()


async def add_request_data(data: dict, session: AsyncSession) -> None:
    try:
        request_data = CheckRequestSchema(**data)
    except ValidationError as e:
        raise ValueError(e.json())

    request_data = Request(**data)

    session.add(request_data)
    await session.commit()
