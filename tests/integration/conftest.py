import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="function")
async def admin_user_token(async_client) -> dict:
    user_data_login = {
        "email": "admin@gmail.com",
        "password": "admin_password",
    }
    response = await async_client.post("/users/login", data=user_data_login)

    assert response.status_code == 200, "Admin login failed"
    data = response.json()
    return data


@pytest_asyncio.fixture(scope="function")
async def homer_user_token(async_client) -> dict:
    user_data_login = {
        "email": "homer@gmail.com",
        "password": "homer_password",
    }
    response = await async_client.post("/users/login", data=user_data_login)

    assert response.status_code == 200, "Homer login failed"
    data = response.json()
    return data


# user fixture
@pytest.fixture()
def user_data():
    return {
        "first_name": "testUser",
        "last_name": "testUser",
        "email": "testuser@gmail.com",
        "phone_number": "+380960220115",
        "password": "qwerty1",
    }


@pytest.fixture()
def user_login_data():
    return {
        "email": "testuser@gmail.com",
        "password": "qwerty1",
    }


@pytest.fixture()
def new_user_data():
    return {
        "first_name": "new_user",
        "phone_number": "+380960334987",
    }


@pytest.fixture()
def authorization_admin(admin_user_token):
    return {"Authorization": f"Bearer {admin_user_token['access_token']}"}


@pytest.fixture()
def authorization_homer(homer_user_token):
    return {"Authorization": f"Bearer {homer_user_token['access_token']}"}


# dish fixture
@pytest.fixture()
def dish_data():
    return {
        "name": "cheeseburger",
        "price": 100,
        "category_id": 1,
    }


@pytest.fixture()
def new_dish_data():
    return {
        "description": "new cheeseburger",
    }
