from src.repositories.payment_repository import PaymentRepository
from src.repositories.order_repository import OrderRepository
from src.repositories.cart_repository import CartRepository
from src.services.base_service import AbstractService
from sqlalchemy.ext.asyncio import AsyncSession
from src.exceptions import NotFoundError
from src.core import db_helper
from typing import Annotated
from fastapi import Depends
from src.schemas.order_schemas import (
    CreateOrderSchema,
    PaymentMethod,
    AddCreatedOrderSchema,
)


class OrderService(AbstractService):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
    ):
        self._order_repository = OrderRepository(session)
        self._cart_repository = CartRepository(session)
        self._payment_repository = PaymentRepository(session)

    async def add(self, data: CreateOrderSchema, user_id: int):
        # 1. Отримати всі cart items
        cart_items = await self._cart_repository.find_cart(user_id=user_id)
        if not cart_items:
            raise NotFoundError("Cart not found")

        order_items = []
        for cart_item in cart_items:
            price = cart_item.dish.price

            order_item = self._order_repository.create_order_items_instance(
                dish_id=cart_item.dish.id, quantity=cart_item.quantity, price=price
            )
            order_items.append(order_item)

        # 2. Порахувати загальну суму
        total_price = await self._cart_repository.calculate_total(user_id=user_id)

        # 3. Створити платіж
        payment = self._payment_repository.create_instance(
            payment_method=data.payment_method,
            total_price=total_price,
            paid=(data.payment_method != PaymentMethod.cash),
        )

        # 4. Створити замовлення
        await self._order_repository.create(
            AddCreatedOrderSchema(user_id=user_id, payment=payment, items=order_items)
        )

        # 5. Очистити кошик
        await self._cart_repository.delete(user_id=user_id)

    async def update(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass

    async def get(self, **kwargs):
        if not (order := await self._order_repository.find_single(**kwargs)):
            raise NotFoundError("Order not found")
        return order
