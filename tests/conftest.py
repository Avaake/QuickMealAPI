from tests.utils import (
    AsyncSessionGenerator,
    async_session_maker,
    ClientManagerType,
    client_manager,
    engine_test,
    metadata,
)
from src.main import app
import pytest_asyncio


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSessionGenerator:
    async with async_session_maker() as session:
        async with session.begin():
            yield session


@pytest_asyncio.fixture(scope="module", autouse=True)
async def engine():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield engine_test
    await engine_test.dispose()
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c
