from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from core.config import settings
from typing import AsyncGenerator


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=echo,
            pool_size=pool_size,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
        )
        self.async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, autocommit=False, autoflush=False
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session

    @asynccontextmanager
    async def get_db(self):
        session = self.async_session_maker()
        try:
            yield session
        finally:
            await session.close()


db_helper = DatabaseHelper(
    url=str(settings.db.database_url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
