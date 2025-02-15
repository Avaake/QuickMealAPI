from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_schema import CreateUserSchema
from src.repositories.user_repositry import UserRepository
from src.core import User, db_helper
from src.exceptions import (
    UserAlreadyExistsError,
    NotFoundError,
)
from src.services.base_service import AbstractService

from jose import jwt
import bcrypt
from src.core import settings
from datetime import datetime, timedelta
import uuid
from typing import Annotated
from fastapi import Depends


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

    async def update(self):
        pass

    async def delete(self):
        pass

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
        expire_minutes: int = settings.auth_jwt.access_token_expire_day,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
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
            token_type="access",
            payload=payload,
            expire_minutes=settings.auth_jwt.access_token_expire_day,
        )

    def create_refresh_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
        }
        return self.create_token(
            token_type="refresh",
            payload=payload,
            expire_minutes=settings.auth_jwt.refresh_token_expire_day,
        )
