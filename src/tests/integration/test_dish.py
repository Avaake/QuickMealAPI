import pytest
from sqlalchemy import select
from core import Dish


@pytest.mark.asyncio
class TestDish:
    async def test_create_dish(
        self, async_client, authorization_admin, db_session, dish_data
    ):
        response = await async_client.post(
            "/dishes",
            json=dish_data,
            headers=authorization_admin,
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

    async def test_create_dish_forbidden_not_enough_rights(
        self, async_client, authorization_homer, dish_data
    ):
        response = await async_client.post(
            "/dishes",
            json=dish_data,
            headers=authorization_homer,
        )

        assert response.status_code == 403
        data = response.json()
        assert data["detail"] == "Not enough rights"

    async def test_create_dish_validate_error(
        self, async_client, authorization_admin, dish_data
    ):
        response = await async_client.post(
            "/dishes",
            json={"price": 0},
            headers=authorization_admin,
        )

        assert response.status_code == 422

    async def test_get_all_dishes(self, async_client):
        response = await async_client.get("/dishes")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 1

    async def test_get_all_dishes_with_query(self, async_client):
        response = await async_client.get(
            "/dishes?category_id=1&order_by=true",
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["category_id"] == 1

    async def test_gat_dish(self, async_client):
        response = await async_client.get(
            "/dishes/3",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "cheeseburger"

    async def test_get_dish_not_found(self, async_client):
        response = await async_client.get(
            "/dishes/111",
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Dish not found"

    async def test_update_dish(
        self, async_client, authorization_admin, db_session, new_dish_data
    ):
        response = await async_client.patch(
            "/dishes/3",
            json=new_dish_data,
            headers=authorization_admin,
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

    async def test_update_dish_forbidden_not_enough_rights(
        self, async_client, authorization_homer, new_dish_data
    ):
        response = await async_client.patch(
            "/dishes/3",
            json=new_dish_data,
            headers=authorization_homer,
        )
        assert response.status_code == 403
        data = response.json()
        assert data["detail"] == "Not enough rights"

    async def test_delete_dish(self, async_client, authorization_admin, db_session):
        response = await async_client.delete(
            "/dishes/3",
            headers=authorization_admin,
        )
        assert response.status_code == 204

        stmt = select(Dish).where(Dish.id == 3)
        result = await db_session.execute(stmt)
        category = result.scalars().first()

        assert category is None
