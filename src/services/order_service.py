from datetime import datetime

from repositories.payment_repository import PaymentRepository
from repositories.order_repository import OrderRepository
from repositories.cart_repository import CartRepository
from services.base_service import AbstractService
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import NotFoundError
from core import db_helper
from typing import Annotated
from fastapi import Depends
from schemas.order_schemas import (
    CreateOrderSchema,
    PaymentMethod,
    AddCreatedOrderInstanceSchema,
    UpdateOrderSchema,
    ReadOrderSchema,
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
            paid=False,
        )

        # 4. Створити замовлення
        await self._order_repository.create(
            AddCreatedOrderInstanceSchema(
                user_id=user_id, payment=payment, items=order_items
            )
        )

        # 5. Очистити кошик
        await self._cart_repository.delete(user_id=user_id)

        order = await self.get(user_id=user_id, payment_id=payment.id)
        return order

    async def update(self, order_data: UpdateOrderSchema, order_id: int):
        await self.get(order_id=order_id)
        return await self._order_repository.update(data=order_data, order_id=order_id)

    async def delete(self, **kwargs):
        pass

    async def get(self, **kwargs):
        if not (order := await self._order_repository.find_single(**kwargs)):
            raise NotFoundError("Order not found")
        return order
