from typing import Sequence, Optional
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.core import db_helper, Dish
from src.services.base_service import AbstractService
from fastapi import Depends
from src.repositories.dish_repository import DishRepository
from src.exceptions import DishAlreadyExistsError, NotFoundError


class DishService(AbstractService):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
    ):
        self._dish_repository = DishRepository(session)

    async def add(self, dish_data) -> Dish:
        if await self._dish_repository.find_single(name=dish_data.name):
            raise DishAlreadyExistsError("User already exists")

        return await self._dish_repository.create(data=dish_data)

    async def update(self, dish_id: int, dish_data) -> Dish:
        await self.get(id=dish_id)
        return await self._dish_repository.update(id=dish_id, data=dish_data)

    async def delete(self, dish_id: int) -> None:
        await self.get(id=dish_id)
        await self._dish_repository.delete(id=dish_id)

    async def get(self, **kwargs) -> Dish:
        if not (dish := await self._dish_repository.find_single(**kwargs)):
            raise NotFoundError("User not found")
        return dish

    async def get_all(
        self, category_id: Optional[int] = None, order_by: bool = False
    ) -> Sequence[Dish]:
        return await self._dish_repository.find_all(
            order_by=order_by, category_id=category_id
        )
