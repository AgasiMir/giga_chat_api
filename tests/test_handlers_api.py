import pytest
from httpx import AsyncClient

async def test_handlers(ac: AsyncClient):
    response = await ac.get("handlers/check_db")
    assert response.status_code == 200
    assert response.json()['response'] == 'Hello World!'

