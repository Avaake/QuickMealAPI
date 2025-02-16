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

    response = await async_client.post("/api/v1/users/register", json=user_data)

    data = response.json()
    assert response.status_code == 201
    assert data["email"] == "testuser@gmail.com"

    stmt = select(User).where(User.email == "testuser@gmail.com")
    result = await db_session.execute(stmt)
    user = result.scalars().first()

    assert user is not None
