from main import main_app
import pytest_asyncio
from tests.utils import (
    async_session_maker,
    insert_into_tables,
    ClientManagerType,
    client_manager,
    engine_test,
    metadata,
)
from core import settings

app = main_app


@pytest_asyncio.fixture(scope="module", autouse=True)
async def engine():
    assert settings.mode == "TEST"
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)

    await insert_into_tables()

    yield

    await engine_test.dispose()
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c
