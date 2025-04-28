import pytest
from sqlalchemy import select
from core import CartItem


@pytest.mark.asyncio
class TestCart:

    async def test_add_to_cart(self, async_client, authorization_homer, db_session):
        response = await async_client.post(
            "/carts/add",
            json={
                "dish_id": 1,
                "quantity": 10,
            },
            headers=authorization_homer,
        )

        assert response.status_code == 200
        data = response.json()

        assert data["message"] == "Dish added to cart."

        stmt = select(CartItem).where(CartItem.user_id == 2, CartItem.dish_id == 1)
        result = await db_session.execute(stmt)
        cart = result.scalars().first()

        assert cart is not None
        assert cart.dish_id == 1

    async def test_add_to_cart_exc_not_found(
        self, async_client, authorization_homer, db_session
    ):
        response = await async_client.post(
            "/carts/add",
            json={
                "dish_id": 10,
                "quantity": 2,
            },
            headers=authorization_homer,
        )

        assert response.status_code == 400
        data = response.json()

        assert data["detail"] == "Dish not found"

    async def test_remove_from_cart(
        self, async_client, authorization_homer, db_session
    ):
        response = await async_client.delete(
            "/carts/remove/2",
            headers=authorization_homer,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Dish removed from cart."

        stmt = select(CartItem).where(CartItem.user_id == 2, CartItem.dish_id == 2)
        result = await db_session.execute(stmt)
        cart = result.scalars().first()

        assert cart is None

    async def test_get_total_price(self, async_client, authorization_homer):
        response = await async_client.get(
            "/carts/total-price",
            headers=authorization_homer,
        )

        assert response.status_code == 200
        data = response.json()
        assert "total_price" in data
        assert data["total_price"] is not None

    async def test_get_cart(self, async_client, authorization_homer):
        response = await async_client.get(
            "/carts",
            headers=authorization_homer,
        )

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["name"] == "fish_burger"

    async def test_clear_cart(self, async_client, authorization_homer, db_session):
        response = await async_client.delete(
            "/carts/clear",
            headers=authorization_homer,
        )
        assert response.status_code == 204

        stmt = select(CartItem).where(CartItem.user_id == 2, CartItem.dish_id == 1)
        result = await db_session.execute(stmt)
        cart = result.scalars().first()

        assert cart is None
