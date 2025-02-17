from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from src.core import Base, settings
from typing import AsyncGenerator
from sqlalchemy import NullPool


ClientManagerType = AsyncGenerator[AsyncClient, None]
AsyncSessionGenerator = AsyncGenerator[AsyncSession, None]
metadata = Base.metadata
DATABASE_URL = str(settings.db.database_url)

engine_test = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def client_manager(app, base_url="http://test", **kwargs) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url=base_url, **kwargs) as c:
            yield c
