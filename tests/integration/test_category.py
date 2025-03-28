import pytest
from sqlalchemy import select
from src.core import Category


@pytest.mark.asyncio
async def test_create_new_category(async_client, admin_user_token, db_session):
    category_data = {
        "name": "Test Category",
        "description": "Test description",
    }

    response = await async_client.post(
        "/categories",
        json=category_data,
        headers={
            "Authorization": f"Bearer {admin_user_token['access_token']}",
        },
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


@pytest.mark.asyncio
async def test_create_category_forbidden_not_enough_rights(
    async_client, homer_user_token
):
    category_data = {
        "name": "Test Category",
        "description": "Test description",
    }

    response = await async_client.post(
        "/categories",
        json=category_data,
        headers={
            "Authorization": f"Bearer {homer_user_token['access_token']}",
        },
    )

    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Not enough rights"


@pytest.mark.asyncio
async def test_create_category_validate_error(async_client, admin_user_token):
    category_data = {
        "description": "Test description",
    }

    response = await async_client.post(
        "/categories",
        json=category_data,
        headers={
            "Authorization": f"Bearer {admin_user_token['access_token']}",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_categories(async_client):
    response = await async_client.get("/categories")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 1


@pytest.mark.asyncio
async def test_get_category(async_client):
    response = await async_client.get("/categories/3")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 3
    assert data["name"] == "Test Category"
    assert data["description"] == "Test description"


@pytest.mark.asyncio
async def test_update_category(async_client, admin_user_token, db_session):
    category_data = {
        "name": "New Test Category",
    }
    response = await async_client.patch(
        "/categories/3",
        json=category_data,
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
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


@pytest.mark.asyncio
async def test_update_category_forbidden_not_enough_rights(
    async_client, homer_user_token
):
    category_data = {
        "name": "New Test Category",
    }
    response = await async_client.patch(
        "/categories/3",
        json=category_data,
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )

    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Not enough rights"


@pytest.mark.asyncio
async def test_update_category_not_found_error(async_client, admin_user_token):
    category_data = {
        "name": "New Test Category",
    }
    response = await async_client.patch(
        "/categories/22",
        json=category_data,
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Category not found"


@pytest.mark.asyncio
async def test_delete_category(async_client, admin_user_token, db_session):
    response = await async_client.delete(
        "/categories/3",
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )

    assert response.status_code == 204

    stmt = select(Category).where(Category.id == 2)
    result = await db_session.execute(stmt)
    category = result.scalars().first()

    assert category is None


@pytest.mark.asyncio
async def test_delete_category_forbidden_not_enough_rights(
    async_client, homer_user_token
):
    response = await async_client.delete(
        "/categories/3",
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Not enough rights"


@pytest.mark.asyncio
async def test_delete_category_not_found_error(async_client, admin_user_token):
    response = await async_client.delete(
        "/categories/22",
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Category not found"
