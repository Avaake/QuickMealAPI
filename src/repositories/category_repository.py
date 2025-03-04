from typing import Union, Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository, ModelType
from sqlalchemy.ext.asyncio import AsyncSession
from src.core import Category


class CategoryRepository(SQLAlchemyRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def find_single(self, **filters) -> Union[ModelType, None]:
        res = await self._session.execute(
            select(self.model)
            .options(selectinload(self.model.dishes))
            .filter_by(**filters)
        )
        return res.scalar_one_or_none()

    async def find_all(self) -> Sequence[ModelType]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.dishes))
            .order_by(self.model.id)
        )
        res = await self._session.execute(stmt)
        return res.scalars().all()
