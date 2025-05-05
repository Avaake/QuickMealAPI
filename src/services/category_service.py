from exceptions import AlreadyExistsError, NotFoundError
from repositories.sqlalchemy_repository import ModelType
from services.base_service import AbstractService
from typing import Annotated, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core import db_helper, Category
from repositories.category_repository import CategoryRepository
from schemas.category_schema import CategoryBaseSchema, UpdateCategorySchema


class CategoryService(AbstractService):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
    ):
        self._category_repository = CategoryRepository(session)

    async def add(self, category_data: CategoryBaseSchema) -> Category:
        if await self._category_repository.find_single(name=category_data.name):
            raise AlreadyExistsError("Category already exists")

        category = await self._category_repository.create(data=category_data)
        return category

    async def update(
        self, category_id: int, category_data: UpdateCategorySchema
    ) -> Category:
        await self.get(id=category_id)
        category = await self._category_repository.update(
            id=category_id, data=category_data
        )
        return category

    async def delete(self, category_id: int) -> None:
        await self.get(id=category_id)
        await self._category_repository.delete(id=category_id)

    async def get(self, **kwargs) -> Category:
        if not (category := await self._category_repository.find_single(**kwargs)):
            raise NotFoundError("Category not found")
        return category

    async def get_all(self) -> Sequence[ModelType]:
        return await self._category_repository.find_all()
