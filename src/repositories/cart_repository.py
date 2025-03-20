from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from core import CartItem, Dish
from src.schemas.cart_schemas import CreateCartSchema
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository, ModelType
from sqlalchemy.ext.asyncio import AsyncSession
from src.core import CartItem


class CartRepository(SQLAlchemyRepository[CartItem]):
    def __init__(self, session: AsyncSession):
        super().__init__(CartItem, session)

    async def add_item(self, user_id: int, dish_id: int, quantity: int):
        existing_item = await self.find_single(user_id=user_id, dish_id=dish_id)

        if existing_item:
            existing_item.quantity = quantity
            await self._session.commit()
        else:
            await self.create(
                CreateCartSchema(user_id=user_id, dish_id=dish_id, quantity=quantity)
            )

    async def find_cart(self, user_id: int) -> Sequence[CartItem]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.dish))
            .filter_by(user_id=user_id)
        )
        res = await self._session.execute(stmt)
        return res.scalars().all()

    async def calculate_total(self, user_id: int) -> int:
        stmt = (
            select(func.sum(CartItem.quantity * Dish.price))
            .join(Dish)
            .filter(CartItem.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        total = result.scalar() or 0
        return total
