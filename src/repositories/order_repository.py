from typing import Union

from sqlalchemy import select

from repositories.sqlalchemy_repository import SQLAlchemyRepository, ModelType
from sqlalchemy.ext.asyncio import AsyncSession
from core import Order, OrderItem
from sqlalchemy.orm import selectinload


class OrderRepository(SQLAlchemyRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    @staticmethod
    def create_order_items_instance(
        dish_id: int, quantity: int, price: int
    ) -> OrderItem:
        return OrderItem(
            dish_id=dish_id,
            quantity=quantity,
            price=price,
        )

    async def find_single(self, **filters) -> Union[ModelType, None]:
        res = await self._session.execute(
            select(self.model)
            .options(selectinload(self.model.items))
            .options(selectinload(self.model.payment))
            .filter_by(**filters)
        )
        return res.scalar_one_or_none()
