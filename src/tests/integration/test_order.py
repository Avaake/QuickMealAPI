import pytest
from core import Order, OrderItem, Payment
from sqlalchemy import select


@pytest.mark.asyncio
class TestOrder:
    async def test_create_order(self, async_client, db_session, authorization_homer):
        response = await async_client.post(
            "/orders",
            json={"payment_method": "cash"},
            headers=authorization_homer,
        )

        assert response.status_code == 201
        data = response.json()

        assert data is not None
        assert data["user_id"] == 2
        assert data["status"] == "pending"
        # data/payment
        assert isinstance(data["payment"], dict)
        assert "method" in data["payment"]
        assert "amount" in data["payment"]
        assert "paid" in data["payment"]
        # data/items
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 1
        assert "order_id" in data["items"][0]
        assert "dish_id" in data["items"][0]
        assert "quantity" in data["items"][0]
        assert "price" in data["items"][0]

        stmt = select(Order).where(Order.user_id == 2)
        result = await db_session.execute(stmt)
        order: "Order" = result.scalar_one_or_none()

        assert order is not None
        assert order.user_id == 2
        assert order.payment_id == 1
        assert order.status == "pending"

        stmt = select(OrderItem).where(OrderItem.order_id == order.id)
        result = await db_session.execute(stmt)
        order_items: "OrderItem" = result.scalar_one_or_none()

        assert order_items is not None
        assert order_items.order_id == 1
        assert order_items.dish_id == 2
        assert order_items.quantity == 8
        assert order_items.price == 299

        stmt = select(Payment).where(Payment.id == order.payment_id)
        result = await db_session.execute(stmt)
        payment: "Payment" = result.scalar_one_or_none()

        assert payment is not None
        assert payment.method == "cash"
        assert payment.amount == 2392
        assert payment.paid == False

    async def test_update_order(self, async_client, db_session, authorization_admin):
        response = await async_client.put(
            "/orders/1",
            json={"status": "delivered"},
            headers=authorization_admin,
        )
        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "delivered"

        stmt = select(Order).where(Order.user_id == 2)
        result = await db_session.execute(stmt)
        order: "Order" = result.scalar_one_or_none()

        assert order is not None
        assert order.user_id == 2
        assert order.payment_id == 1
        assert order.status == "delivered"
