import pytest_asyncio
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def fastapi_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
