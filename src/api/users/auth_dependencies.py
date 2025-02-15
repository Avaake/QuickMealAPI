from fastapi import Depends, HTTPException, status, Form
from src.services.user_service import UserService
from src.schemas.user_schema import LoginSchema
from src.core import User
from src.exceptions import (
    UNAUTHORIZED_EXC,
    FORBIDDEN_EXC,
    TOKEN_INVALID_EXC,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from typing import Annotated
from jose import JWTError


http_bearer = HTTPBearer(auto_error=False)


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def get_current_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    user_service: Annotated["UserService", Depends(UserService)],
) -> dict:
    token = credentials.credentials
    try:
        payload = user_service.decode_token(
            token=token,
        )
    except JWTError:
        raise TOKEN_INVALID_EXC
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub_and_email(
    payload: dict,
    user_service: Annotated["UserService", Depends(UserService)],
) -> User:
    sub: str | None = payload["sub"]
    email: str | None = payload.get("email")
    if user := await user_service.get(id=int(sub), email=email):
        return user
    raise TOKEN_INVALID_EXC


def get_auth_user_from_token_of_type(token_type: str):

    async def get_auth_user_from_token(
        user_service: Annotated["UserService", Depends(UserService)],
        payload: dict = Depends(get_current_token_payload),
    ) -> User:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub_and_email(payload, user_service)

    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


def ger_current_active_user(
    user: Annotated[User, Depends(get_current_auth_user)],
):
    if user.is_active:
        return user
    raise FORBIDDEN_EXC


async def authenticate_user(
    user_data: Annotated[LoginSchema, Form()],
    user_service: Annotated["UserService", Depends(UserService)],
) -> User:
    if not (user := await user_service.get(email=user_data.email)):
        raise UNAUTHORIZED_EXC

    if not user_service.verify_password(
        password=user_data.password, hashed_password=user.password
    ):
        raise UNAUTHORIZED_EXC

    if not user.is_active:
        raise FORBIDDEN_EXC
    return user
