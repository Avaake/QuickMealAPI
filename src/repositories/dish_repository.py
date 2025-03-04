from src.repositories.sqlalchemy_repository import SQLAlchemyRepository, ModelType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from sqlalchemy.orm import selectinload
from typing import Union, Sequence
from src.core import Dish


class DishRepository(SQLAlchemyRepository[Dish]):
    def __init__(self, session: AsyncSession):
        super().__init__(Dish, session)

    async def find_single(self, **filters) -> Union[ModelType, None]:
        res = await self._session.execute(
            select(self.model)
            .options(selectinload(self.model.category))
            .filter_by(**filters)
        )
        return res.scalar_one_or_none()

    async def find_all(self, order_by: bool = False, **kwargs) -> Sequence[ModelType]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.category))
            .filter_by(**kwargs)
            .order_by(asc(self.model.price) if order_by else desc(self.model.price))
        )

        res = await self._session.execute(stmt)
        return res.scalars().all()
