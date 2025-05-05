from schemas.user_schema import LoginSchema, UpdateUserSchema
from fastapi import Depends, HTTPException, status, Form, Path
from services.user_service import (
    UserService,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from exceptions import (
    FORBIDDEN_EXC_NOT_ENOUGH_RIGHTS,
    UNAUTHORIZED_EXC_INCORRECT,
    FORBIDDEN_EXC_INACTIVE,
    TOKEN_INVALID_EXC,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from typing import Annotated
from jose import JWTError
from core import User


http_bearer = HTTPBearer(auto_error=False)


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
    current_token_type = payload.get("type")
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
    # email: str | None = payload.get("email")
    if user := await user_service.get(id=int(sub)):
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


def check_user_is_active(
    user: Annotated[User, Depends(get_current_auth_user)],
) -> User:
    if not user.is_active:
        raise FORBIDDEN_EXC_INACTIVE
    return user


async def check_user_is_admin(
    user: Annotated[User, Depends(get_current_auth_user)],
) -> User:
    if not user.is_admin:
        raise FORBIDDEN_EXC_NOT_ENOUGH_RIGHTS
    return user


async def authenticate_user(
    user_data: Annotated[LoginSchema, Form()],
    user_service: Annotated["UserService", Depends(UserService)],
) -> User:
    if not (user := await user_service.get(email=user_data.email)):
        raise UNAUTHORIZED_EXC_INCORRECT

    if not user_service.verify_password(
        password=user_data.password, hashed_password=user.password
    ):
        raise UNAUTHORIZED_EXC_INCORRECT

    if not user.is_active:
        raise FORBIDDEN_EXC_INACTIVE

    return user


async def user_is_admin_or_user_himself(
    user_id: Annotated[int, Path(ge=1)],
    user_data: UpdateUserSchema,
    user: Annotated[User, Depends(get_current_auth_user)],
) -> User:

    if not user.is_admin and user.id != user_id:
        raise FORBIDDEN_EXC_NOT_ENOUGH_RIGHTS

    if not user.is_admin and (
        user_data.is_admin is not None or user_data.is_active is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough rights to change admin or active status",
        )

    return user


async def check_user_is_courier_or_is_admin(
    user: Annotated[User, Depends(get_current_auth_user)],
) -> User:
    if not user.is_courier and not user.is_admin:
        raise FORBIDDEN_EXC_NOT_ENOUGH_RIGHTS

    return user
