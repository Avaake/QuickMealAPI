from src.repositories.cart_repository import CartRepository
from src.services.base_service import AbstractService
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.cart_schemas import (
    BaseCartSchema,
    ReadCartDishSchema,
)
from src.core import db_helper
from typing import Annotated
from fastapi import Depends


class CartService(AbstractService):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
    ):
        self._cart_repository = CartRepository(session)

    async def add(self, user_id: int, cart_data: BaseCartSchema):
        return await self._cart_repository.add_item(
            user_id, cart_data.dish_id, cart_data.quantity
        )

    async def update(self, user_id: int, dish_id: int):
        return await self._cart_repository.delete(user_id=user_id, dish_id=dish_id)

    async def delete(self, user_id: int) -> None:
        return await self._cart_repository.delete(user_id=user_id)

    async def get(self, user_id: int) -> list[ReadCartDishSchema]:
        cart = await self._cart_repository.find_cart(user_id=user_id)
        return [
            ReadCartDishSchema(dish_id=i.dish_id, quantity=i.quantity, name=i.dish.name)
            for i in cart
        ]

    async def calculate_total(self, user_id: int):
        return await self._cart_repository.calculate_total(user_id=user_id)
