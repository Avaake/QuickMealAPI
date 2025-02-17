from src.schemas.user_schema import CreateUserSchema, UpdateUserSchema
from src.repositories.user_repositry import UserRepository
from src.services.base_service import AbstractService
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from src.core import User, db_helper
from src.core import settings
from src.exceptions import (
    UserAlreadyExistsError,
    NotFoundError,
)
from typing import Annotated
from fastapi import Depends
from jose import jwt
import bcrypt
import uuid


ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class UserService(AbstractService):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
    ):
        self._user_repository = UserRepository(session)

    async def add(self, user_data: CreateUserSchema) -> User:
        if await self._user_repository.find_single(email=user_data.email):
            raise UserAlreadyExistsError("User already exists")

        user_data.password = self.hash_password(user_data.password)
        user = await self._user_repository.create(data=user_data)
        return user

    async def update(self, user_id: int, user_data: UpdateUserSchema) -> User:
        await self.get(id=user_id)
        user = await self._user_repository.update(data=user_data, id=user_id)
        return user

    async def delete(self, user_id: int) -> None:
        await self.get(id=user_id)
        await self._user_repository.delete(id=user_id)

    async def get(self, **kwargs) -> User:
        if not (user := await self._user_repository.find_single(**kwargs)):
            raise NotFoundError("User not found")
        return user

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    @staticmethod
    def decode_token(
        token: str | bytes,
        algorithm: str = settings.auth_jwt.algorithm,
        public_key: str = settings.auth_jwt.public_key.read_text(),
    ) -> dict:
        return jwt.decode(token, public_key, algorithms=[algorithm])

    @staticmethod
    def create_token(
        token_type: str,
        payload: dict,
        algorithm: str = settings.auth_jwt.algorithm,
        private_kay: str = settings.auth_jwt.private_key.read_text(),
        expire_days: int = settings.auth_jwt.access_token_expire_day,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(days=expire_days)
        to_encode.update(
            type=token_type,
            exp=expire,
            iat=now,
            jti=str(uuid.uuid4()),
        )
        return jwt.encode(to_encode, private_kay, algorithm=algorithm)

    def create_access_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "email": user.email,
        }
        return self.create_token(
            token_type=ACCESS_TOKEN_TYPE,
            payload=payload,
            expire_days=settings.auth_jwt.access_token_expire_day,
        )

    def create_refresh_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
        }
        return self.create_token(
            token_type=REFRESH_TOKEN_TYPE,
            payload=payload,
            expire_days=settings.auth_jwt.refresh_token_expire_day,
        )
