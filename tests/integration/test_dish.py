import pytest
from sqlalchemy import select
from src.core import Dish


@pytest.mark.asyncio
async def test_create_dish(async_client, admin_user_token, db_session):
    dish_data = {
        "name": "cheeseburger",
        "price": 100,
        "category_id": 1,
    }
    response = await async_client.post(
        "/dishes",
        json=dish_data,
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "cheeseburger"
    assert data["price"] == 100
    assert data["category_id"] == 1

    stmt = select(Dish).where(Dish.name == "cheeseburger")
    result = await db_session.execute(stmt)
    dish = result.scalars().first()

    assert dish is not None
    assert dish.name == "cheeseburger"


@pytest.mark.asyncio
async def test_create_dish_forbidden_not_enough_rights(async_client, homer_user_token):
    dish_data = {
        "name": "cheeseburger",
        "price": 100,
        "category_id": 1,
    }

    response = await async_client.post(
        "/dishes",
        json=dish_data,
        headers={
            "Authorization": f"Bearer {homer_user_token['access_token']}",
        },
    )

    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Not enough rights"


@pytest.mark.asyncio
async def test_create_dish_validate_error(async_client, admin_user_token):
    dish_data = {
        "name": "cheeseburger",
        "price": 0,
    }
    response = await async_client.post(
        "/dishes",
        json=dish_data,
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_dishes(async_client):
    response = await async_client.get("/dishes")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 1


@pytest.mark.asyncio
async def test_get_all_dishes_with_query(async_client):
    response = await async_client.get(
        "/dishes?category_id=1&order_by=true",
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["category_id"] == 1


@pytest.mark.asyncio
async def test_gat_dish(async_client):
    response = await async_client.get(
        "/dishes/3",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "cheeseburger"


@pytest.mark.asyncio
async def test_get_dish_not_found(async_client):
    response = await async_client.get(
        "/dishes/111",
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Dish not found"


@pytest.mark.asyncio
async def test_update_dish(async_client, admin_user_token, db_session):
    dish_data = {
        "description": "new cheeseburger",
    }
    response = await async_client.patch(
        "/dishes/3",
        json=dish_data,
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "cheeseburger"
    assert data["description"] == "new cheeseburger"

    stmt = select(Dish).where(Dish.name == "cheeseburger")
    result = await db_session.execute(stmt)
    dish = result.scalars().first()

    assert dish is not None
    assert dish.description == "new cheeseburger"


@pytest.mark.asyncio
async def test_update_dish_forbidden_not_enough_rights(async_client, homer_user_token):
    dish_data = {
        "description": "new cheeseburger",
    }
    response = await async_client.patch(
        "/dishes/3",
        json=dish_data,
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Not enough rights"


@pytest.mark.asyncio
async def test_delete_dish(async_client, admin_user_token, db_session):
    response = await async_client.delete(
        "/dishes/3",
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )
    assert response.status_code == 204

    stmt = select(Dish).where(Dish.id == 3)
    result = await db_session.execute(stmt)
    category = result.scalars().first()

    assert category is None
