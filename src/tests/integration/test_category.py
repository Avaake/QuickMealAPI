import pytest
from sqlalchemy import select
from core import Category


@pytest.mark.asyncio
class TestCategory:

    async def test_create_new_category(
        self, async_client, authorization_admin, db_session, category_data
    ):
        response = await async_client.post(
            "/categories",
            json=category_data,
            headers=authorization_admin,
        )

        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["name"] == "Test Category"
        assert data["description"] == "Test description"

        stmt = select(Category).where(Category.id == data["id"])
        result = await db_session.execute(stmt)
        category = result.scalars().first()

        assert category is not None

    async def test_create_category_forbidden_not_enough_rights(
        self, async_client, authorization_homer, category_data
    ):
        response = await async_client.post(
            "/categories",
            json=category_data,
            headers=authorization_homer,
        )

        assert response.status_code == 403
        data = response.json()
        assert data["detail"] == "Not enough rights"

    async def test_create_category_validate_error(
        self, async_client, authorization_admin
    ):

        response = await async_client.post(
            "/categories",
            json={"description": "Test description"},
            headers=authorization_admin,
        )

        assert response.status_code == 422

    async def test_get_all_categories(self, async_client):
        response = await async_client.get("/categories")

        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 1

    async def test_get_category(self, async_client):
        response = await async_client.get("/categories/3")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == 3
        assert data["name"] == "Test Category"
        assert data["description"] == "Test description"

    async def test_update_category(
        self, async_client, authorization_admin, db_session, new_category_data
    ):
        response = await async_client.patch(
            "/categories/3",
            json=new_category_data,
            headers=authorization_admin,
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == 3
        assert data["name"] == "New Test Category"

        stmt = select(Category).where(Category.id == data["id"])
        result = await db_session.execute(stmt)
        category = result.scalars().first()

        assert category.id == data["id"]
        assert category.name == "New Test Category"

    async def test_update_category_forbidden_not_enough_rights(
        self, async_client, authorization_homer, new_category_data
    ):
        response = await async_client.patch(
            "/categories/3",
            json=new_category_data,
            headers=authorization_homer,
        )

        assert response.status_code == 403
        data = response.json()
        assert data["detail"] == "Not enough rights"

    async def test_update_category_not_found_error(
        self, async_client, authorization_admin, new_category_data
    ):
        response = await async_client.patch(
            "/categories/22",
            json=new_category_data,
            headers=authorization_admin,
        )

        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Category not found"

    async def test_delete_category(self, async_client, authorization_admin, db_session):
        response = await async_client.delete(
            "/categories/3",
            headers=authorization_admin,
        )

        assert response.status_code == 204

        stmt = select(Category).where(Category.id == 3)
        result = await db_session.execute(stmt)
        category = result.scalars().first()

        assert category is None

    async def test_delete_category_forbidden_not_enough_rights(
        self, async_client, authorization_homer
    ):
        response = await async_client.delete(
            "/categories/3",
            headers=authorization_homer,
        )
        assert response.status_code == 403
        data = response.json()
        assert data["detail"] == "Not enough rights"

    async def test_delete_category_not_found_error(
        self, async_client, authorization_admin
    ):
        response = await async_client.delete(
            "/categories/22",
            headers=authorization_admin,
        )

        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Category not found"
