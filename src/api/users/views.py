from src.schemas.user_schema import CreateUserSchema, TokenInfo, ReadUserSchema
from src.api.users.decorators import handle_users_error_decorator
from src.services.user_service import UserService
from src.api.users.auth_dependencies import (
    authenticate_user,
    get_current_auth_user,
    get_current_auth_user_for_refresh,
    http_bearer,
)
from fastapi import APIRouter, Depends
from src.core import User, settings
from typing import Annotated

router = APIRouter(
    prefix=settings.api_prefix.users,
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register", status_code=201, summary="create new user")
@handle_users_error_decorator
async def register(
    user_data: CreateUserSchema,
    user_service: Annotated["UserService", Depends(UserService)],
) -> ReadUserSchema:
    user = await user_service.add(user_data)
    return ReadUserSchema(**user.to_dict())


@router.post("/login", status_code=200, summary="login user")
@handle_users_error_decorator
async def auth_user_issue_jwt(
    user: Annotated[User, Depends(authenticate_user)],
    user_service: Annotated["UserService", Depends(UserService)],
):
    access_token = user_service.create_access_token(user)
    refresh_token = user_service.create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary="refresh user",
    status_code=200,
)
@handle_users_error_decorator
async def create_new_access_token(
    user: Annotated[
        User,
        Depends(
            get_current_auth_user_for_refresh,
        ),
    ],
    user_service: Annotated["UserService", Depends(UserService)],
):
    access_token = user_service.create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/me", summary="get current user", status_code=200)
@handle_users_error_decorator
async def auth_user_check_self_info(
    user: Annotated[User, Depends(get_current_auth_user)],
):
    return ReadUserSchema(**user.to_dict())
