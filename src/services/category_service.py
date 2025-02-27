from src.services.base_service import AbstractService
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.core import db_helper, Category
from src.repositories.category_repository import CategoryRepository
from src.schemas.category_schema import CategoryBaseSchema, UpdateCategorySchema


class CategoryService(AbstractService):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
    ):
        self._user_repository = CategoryRepository(session)

    async def add(self, category_data: CategoryBaseSchema) -> Category:
        pass

    async def update(
        self, category_id: int, category_data: UpdateCategorySchema
    ) -> Category:
        pass

    async def delete(self, category_id: int) -> None:
        pass

    async def get(self, category_id: int) -> None:
        pass

    async def get_all(self) -> list[Category]:
        pass
