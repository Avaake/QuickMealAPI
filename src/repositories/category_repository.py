from src.repositories.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.core import Category


class CategoryRepository(SQLAlchemyRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)
