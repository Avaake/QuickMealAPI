from repositories.base_repository import BaseRepository
from typing import TypeVar, Generic, Type, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from pydantic import BaseModel
from core import Base


ModelType = TypeVar("ModelType", bound=Base)


class SQLAlchemyRepository(BaseRepository, Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self._session = session

    async def create(self, data: BaseModel) -> ModelType:
        obj = self.model(**data.model_dump())
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def update(self, data: BaseModel, **filters) -> Union[ModelType, None]:
        stmt = (
            update(self.model)
            .where(
                *[getattr(self.model, key) == value for key, value in filters.items()]
            )
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model.id)
        )

        res = await self._session.execute(stmt)
        await self._session.commit()
        updated_id = res.scalar_one_or_none()

        if updated_id is None:
            return None

        return await self.find_single(id=updated_id)

    async def delete(self, **filters) -> None:
        await self._session.execute(delete(self.model).filter_by(**filters))
        await self._session.commit()

    async def find_single(self, **filters) -> Union[ModelType, None]:
        res = await self._session.execute(select(self.model).filter_by(**filters))
        return res.scalar_one_or_none()
