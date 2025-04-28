import pytest
from sqlalchemy import select
from core import User


@pytest.mark.asyncio
class TestUser:
    async def test_registration(self, async_client, db_session, user_data):
        response = await async_client.post("/users/register", json=user_data)

        data = response.json()
        assert response.status_code == 201
        assert data["email"] == "testuser@gmail.com"

        stmt = select(User).where(User.email == "testuser@gmail.com")
        result = await db_session.execute(stmt)
        user = result.scalars().first()

        assert user is not None

    async def test_error_user_already_exists(self, async_client, user_data):
        response = await async_client.post("/users/register", json=user_data)
        data = response.json()
        assert response.status_code == 400
        assert data["detail"] == "User already exists"

    async def test_login(self, async_client, user_login_data):
        response = await async_client.post("/users/login", data=user_login_data)

        data = response.json()
        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "Bearer"

    async def test_login_incorrect_error(self, async_client):
        user_data = {
            "email": "testuser@gmail.com",
            "password": "test_qwerty1",
        }
        response = await async_client.post("/users/login", data=user_data)
        data = response.json()
        assert response.status_code == 401
        assert data["detail"] == "Incorrect email or password"

    async def test_get_me(self, async_client, user_login_data):
        response = await async_client.post("/users/login", data=user_login_data)
        data = response.json()

        response = await async_client.get(
            "/users/me", headers={"Authorization": f"Bearer {data['access_token']}"}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["email"] == "testuser@gmail.com"

    async def test_create_new_access_token(self, async_client, admin_user_token):
        response = await async_client.post(
            "/users/refresh",
            headers={"Authorization": f"Bearer {admin_user_token['refresh_token']}"},
        )
        data = response.json()
        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" not in data

    async def test_user_updated_the_himself(
        self, async_client, db_session, user_login_data, new_user_data
    ):
        response = await async_client.post("/users/login", data=user_login_data)
        data_user_login = response.json()

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

    async def test_forbidden_to_change_admin_or_active_status_without_rights(
        self, async_client, user_login_data
    ):
        response = await async_client.post("/users/login", data=user_login_data)
        data_user_login = response.json()

        response = await async_client.patch(
            "/users/3",
            json={
                "is_admin": True,
            },
            headers={"Authorization": f"Bearer {data_user_login['access_token']}"},
        )

        data = response.json()
        assert response.status_code == 403
        assert data["detail"] == "Not enough rights to change admin or active status"

    async def test_admin_updated_the_user(
        self, async_client, authorization_admin, db_session
    ):

        response = await async_client.patch(
            "/users/3",
            json={
                "first_name": "new_user2",
                "is_active": False,
            },
            headers=authorization_admin,
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

    async def test_update_user_forbidden_not_enough_rights(
        self, async_client, authorization_homer, db_session
    ):
        response = await async_client.patch(
            "/users/3",
            json={
                "first_name": "new_user23",
            },
            headers=authorization_homer,
        )

        data = response.json()
        assert response.status_code == 403
        assert data["detail"] == "Not enough rights"

        stmt = select(User).where(User.email == "testuser@gmail.com")
        result = await db_session.execute(stmt)
        user = result.scalars().first()

        assert user.first_name != "new_user23"

    async def test_delete_user_forbidden_not_enough_rights(
        self, async_client, authorization_homer, db_session
    ):
        response = await async_client.delete(
            "/users/3",
            headers=authorization_homer,
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Not enough rights"

    async def test_delete_user(self, async_client, authorization_admin, db_session):
        response = await async_client.delete(
            "/users/3",
            headers=authorization_admin,
        )
        assert response.status_code == 204

        stmt = select(User).where(User.email == "testuser@gmail.com")
        result = await db_session.execute(stmt)
        user = result.scalars().first()

        assert user is None
