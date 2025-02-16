from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core import Base, User
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from typing import AsyncGenerator
from sqlalchemy import NullPool


ClientManagerType = AsyncGenerator[AsyncClient, None]
metadata = Base.metadata
DATABASE_URL = "postgresql+asyncpg://admin_test:admin_password_test@localhost:5432/quick_meat_db_test"

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
async def client_manager(app, base_url="http://test", **kw) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c
