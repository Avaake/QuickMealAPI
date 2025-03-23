import pytest
from sqlalchemy import select
from src.core import CartItem


@pytest.mark.asyncio
async def test_add_to_cart(async_client, homer_user_token, db_session):
    cart_data = {
        "dish_id": 1,
        "quantity": 10,
    }
    response = await async_client.post(
        "/carts/add",
        json=cart_data,
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Dish added to cart."

    stmt = select(CartItem).where(CartItem.user_id == 2, CartItem.dish_id == 1)
    result = await db_session.execute(stmt)
    cart = result.scalars().first()

    assert cart is not None
    assert cart.dish_id == 1


@pytest.mark.asyncio
async def test_add_to_cart(async_client, homer_user_token, db_session):
    cart_data = {
        "dish_id": 10,
        "quantity": 2,
    }
    response = await async_client.post(
        "/carts/add",
        json=cart_data,
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )

    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "Dish not found"


@pytest.mark.asyncio
async def test_remove_from_cart(async_client, homer_user_token, db_session):
    response = await async_client.post(
        "/carts/remove/1",
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Dish removed from cart."

    stmt = select(CartItem).where(CartItem.user_id == 2, CartItem.dish_id == 1)
    result = await db_session.execute(stmt)
    cart = result.scalars().first()

    assert cart is None


@pytest.mark.asyncio
async def test_get_total_price(async_client, homer_user_token):
    response = await async_client.post(
        "/carts/total-price",
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_price" in data
    assert data["total_price"] is not None


@pytest.mark.asyncio
async def test_get_cart(async_client, homer_user_token):
    response = await async_client.post(
        "/carts",
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 1
    assert data[0]["name"] == "fish_burger"


@pytest.mark.asyncio
async def test_clear_cart(async_client, homer_user_token, db_session):
    response = await async_client.post(
        "/carts/clear",
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )
    assert response.status_code == 204

    stmt = select(CartItem).where(CartItem.user_id == 2, CartItem.dish_id == 1)
    result = await db_session.execute(stmt)
    cart = result.scalars().first()

    assert cart is None
