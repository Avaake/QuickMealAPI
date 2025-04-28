from repositories.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core import User
from sqlalchemy import select
from typing import Union


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Union[User, None]:
        res = await self._session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()
