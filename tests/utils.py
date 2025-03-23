from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from src.services.user_service import UserService
from src.core import Base, settings, User, Category, Dish, CartItem
from typing import AsyncGenerator
from sqlalchemy import NullPool

ClientManagerType = AsyncGenerator[AsyncClient, None]
AsyncSessionGenerator = AsyncGenerator[AsyncSession, None]
metadata = Base.metadata
DATABASE_URL = str(settings.db.database_url)

engine_test = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def insert_into_tables() -> None:
    async with async_session_maker() as session:
        async with session.begin():
            test_data(session=session)
            await session.commit()


def test_data(session: AsyncSession):
    admin_user = User(
        first_name="admin",
        email="admin@gmail.com",
        phone_number="+380999999999",
        password=UserService.hash_password("admin_password"),
        is_admin=True,
    )
    homer_user = User(
        first_name="homer",
        email="homer@gmail.com",
        phone_number="+380888888888",
        password=UserService.hash_password("homer_password"),
    )
    session.add_all([admin_user, homer_user])

    category_1 = Category(
        name="Burger",
    )

    category_2 = Category(
        name="Pizza",
    )

    session.add_all([category_1, category_2])

    dish_1 = Dish(name="fish_burger", price=122, category=category_1)
    dish_2 = Dish(name="margarita", price=299, category=category_2)

    session.add_all([dish_1, dish_2])

    cart_item_1 = CartItem(user_id=homer_user.id, dish_id=dish_1.id, quantity=2)
    cart_item_2 = CartItem(user_id=homer_user.id, dish_id=dish_2.id, quantity=8)

    session.add_all([cart_item_1, cart_item_2])


@asynccontextmanager
async def client_manager(
    app, base_url="http://test" + settings.api_prefix.api_v1, **kw
) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c
