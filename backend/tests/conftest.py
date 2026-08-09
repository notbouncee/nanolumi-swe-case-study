import os

os.environ["TESTING"] = "1"

import pytest
from typing import cast, Any
from httpx import AsyncClient, ASGITransport
from src.main import app
from tortoise import Tortoise
from src.client.db import TORTOISE_ORM


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    yield
    await Tortoise.close_connections()


@pytest.fixture
async def async_client():
    # ASGITransport automatically runs the FastAPI lifespan which init Tortoise with sqlite://:memory:
    async with AsyncClient(
        transport=ASGITransport(app=cast(Any, app)), base_url="http://test"
    ) as client:
        yield client
