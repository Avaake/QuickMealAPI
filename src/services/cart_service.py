from src.schemas.cart_schemas import BaseCartSchema, UpdateCartSchema
from src.repositories.cart_repository import CartRepository
from src.services.base_service import AbstractService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from src.core import db_helper, CartItem
from typing import Annotated
from fastapi import Depends


class DishService(AbstractService):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
    ):
        self._cart_repository = CartRepository(session)

    async def add(self, cart_item_data: BaseCartSchema):
        return await self._cart_repository.add_item(
            cart_item_data.user_id, cart_item_data.dish_id, cart_item_data.quantity
        )

    async def update(self, cart_item_data: UpdateCartSchema):
        return await self._cart_repository.delete(
            user_id=cart_item_data.user_id, dish_id=cart_item_data.dish_id
        )

    async def delete(self, user_id: int) -> None:
        return await self._cart_repository.delete(user_id=user_id)

    async def get(self, user_id: int) -> Sequence[CartItem]:
        return await self._cart_repository.find_cart(user_id=user_id)

    async def calculate_total(self, user_id: int):
        # cart_items = await self.get(user_id=user_id)
        # return sum(item.quantity * item.dish.price for item in cart_items)
        return await self._cart_repository.calculate_total(user_id=user_id)
