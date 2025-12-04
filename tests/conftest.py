from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.config import Base
from src.database.db_depends import get_session
from src.main import app

async_engine = create_async_engine(
    url="sqlite+aiosqlite:///./test.db",
    echo=False,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
