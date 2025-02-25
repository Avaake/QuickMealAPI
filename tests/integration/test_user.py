import pytest
from sqlalchemy import select
from src.core import User


@pytest.mark.asyncio
async def test_registration(async_client, db_session):
    user_data = {
        "first_name": "testUser",
        "last_name": "testUser",
        "email": "testuser@gmail.com",
        "phone_number": "+380960220115",
        "password": "qwerty1",
    }

    response = await async_client.post("/users/register", json=user_data)

    data = response.json()
    assert response.status_code == 201
    assert data["email"] == "testuser@gmail.com"

    stmt = select(User).where(User.email == "testuser@gmail.com")
    result = await db_session.execute(stmt)
    user = result.scalars().first()

    assert user is not None


@pytest.mark.asyncio
async def test_error_user_already_exists(async_client):
    user_data = {
        "first_name": "testUser",
        "email": "testuser@gmail.com",
        "phone_number": "+380960220115",
        "password": "qwerty1",
    }

    response = await async_client.post("/users/register", json=user_data)
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "User already exists"


@pytest.mark.asyncio
async def test_login(async_client):
    user_data_login = {
        "email": "testuser@gmail.com",
        "password": "qwerty1",
    }
    response = await async_client.post("/users/login", data=user_data_login)

    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_login_incorrect_error(async_client):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "test_qwerty1",
    }
    response = await async_client.post("/users/login", data=user_data)
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_get_me(async_client):
    user_data_login = {
        "email": "testuser@gmail.com",
        "password": "qwerty1",
    }
    response = await async_client.post("/users/login", data=user_data_login)
    data = response.json()

    response = await async_client.get(
        "/users/me", headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == "testuser@gmail.com"


@pytest.mark.asyncio
async def test_create_new_access_token(async_client, admin_user_token):
    response = await async_client.post(
        "/users/refresh",
        headers={"Authorization": f"Bearer {admin_user_token['refresh_token']}"},
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" not in data


@pytest.mark.asyncio
async def test_user_updated_the_himself(async_client, db_session):
    user_data_login = {
        "email": "testuser@gmail.com",
        "password": "qwerty1",
    }
    response = await async_client.post("/users/login", data=user_data_login)
    data_user_login = response.json()

    new_user_data = {
        "first_name": "new_user",
        "phone_number": "+380960334987",
    }
    response = await async_client.patch(
        "/users/3",
        json=new_user_data,
        headers={"Authorization": f"Bearer {data_user_login['access_token']}"},
    )

    data = response.json()
    assert response.status_code == 200
    assert data["first_name"] == "new_user"
    assert data["phone_number"] == "+380960334987"

    stmt = select(User).where(User.email == "testuser@gmail.com")
    result = await db_session.execute(stmt)
    user = result.scalars().first()

    assert user.phone_number == "+380960334987"
    assert user.first_name == "new_user"


@pytest.mark.asyncio
async def test_forbidden_to_change_admin_or_active_status_without_rights(async_client):
    user_data_login = {
        "email": "testuser@gmail.com",
        "password": "qwerty1",
    }
    response = await async_client.post("/users/login", data=user_data_login)
    data_user_login = response.json()

    new_user_data = {
        "is_admin": True,
    }
    response = await async_client.patch(
        "/users/3",
        json=new_user_data,
        headers={"Authorization": f"Bearer {data_user_login['access_token']}"},
    )

    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Not enough rights to change admin or active status"


@pytest.mark.asyncio
async def test_admin_updated_the_user(async_client, admin_user_token, db_session):
    new_user_data = {
        "first_name": "new_user2",
        "is_active": False,
    }
    response = await async_client.patch(
        "/users/3",
        json=new_user_data,
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )

    data = response.json()
    assert response.status_code == 200
    assert data["first_name"] == "new_user2"
    assert data["is_active"] is False

    stmt = select(User).where(User.email == "testuser@gmail.com")
    result = await db_session.execute(stmt)
    user = result.scalars().first()

    assert user.first_name == "new_user2"
    assert user.is_active is False


@pytest.mark.asyncio
async def test_update_user_forbidden_not_enough_rights(
    async_client, homer_user_token, db_session
):
    new_user_data = {
        "first_name": "new_user23",
    }
    response = await async_client.patch(
        "/users/3",
        json=new_user_data,
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )

    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Not enough rights"

    stmt = select(User).where(User.email == "testuser@gmail.com")
    result = await db_session.execute(stmt)
    user = result.scalars().first()

    assert user.first_name != "new_user23"


@pytest.mark.asyncio
async def test_delete_user_forbidden_not_enough_rights(
    async_client, homer_user_token, db_session
):
    response = await async_client.delete(
        "/users/3",
        headers={"Authorization": f"Bearer {homer_user_token['access_token']}"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough rights"


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user_token, db_session):
    response = await async_client.delete(
        "/users/3",
        headers={"Authorization": f"Bearer {admin_user_token['access_token']}"},
    )
    assert response.status_code == 204

    stmt = select(User).where(User.email == "testuser@gmail.com")
    result = await db_session.execute(stmt)
    user = result.scalars().first()

    assert user is None
