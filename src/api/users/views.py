from src.api.decorators import handle_error_decorator
from src.services.user_service import UserService
from fastapi import APIRouter, Depends, Path
from src.api.users.auth_dependencies import (
    get_current_auth_user_for_refresh,
    user_is_admin_or_user_himself,
    get_current_auth_user,
    check_user_is_admin,
    authenticate_user,
    http_bearer,
)
from src.schemas.user_schema import (
    CreateUserSchema,
    TokenInfo,
    ReadUserSchema,
    UpdateUserSchema,
)
from src.core import User, settings
from typing import Annotated

router = APIRouter(
    prefix=settings.api_prefix.users,
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register", status_code=201, summary="create new user")
@handle_error_decorator
async def register(
    user_data: CreateUserSchema,
    user_service: Annotated["UserService", Depends(UserService)],
) -> ReadUserSchema:
    user = await user_service.add(user_data)
    return ReadUserSchema(**user.to_dict())


@router.post("/login", status_code=200, summary="login user")
@handle_error_decorator
async def auth_user_issue_jwt(
    current_user: Annotated[User, Depends(authenticate_user)],
    user_service: Annotated["UserService", Depends(UserService)],
):
    access_token = user_service.create_access_token(current_user)
    refresh_token = user_service.create_refresh_token(current_user)
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
@handle_error_decorator
async def create_new_access_token(
    current_user: Annotated[
        User,
        Depends(
            get_current_auth_user_for_refresh,
        ),
    ],
    user_service: Annotated["UserService", Depends(UserService)],
):
    access_token = user_service.create_access_token(current_user)
    return TokenInfo(access_token=access_token)


@router.get("/me", summary="get current user", status_code=200)
@handle_error_decorator
async def auth_user_check_self_info(
    current_user: Annotated[User, Depends(get_current_auth_user)],
):
    return ReadUserSchema(**current_user.to_dict())


@router.patch("/{user_id}", summary="update user", status_code=200)
@handle_error_decorator
async def update_user(
    user_id: Annotated[int, Path(ge=1)],
    user_data: UpdateUserSchema,
    current_user: Annotated[User, Depends(user_is_admin_or_user_himself)],
    user_service: Annotated["UserService", Depends(UserService)],
) -> ReadUserSchema:
    user = await user_service.update(user_data=user_data, user_id=user_id)
    return ReadUserSchema(**user.to_dict())


@router.delete("/{user_id}", summary="delete user", status_code=204)
@handle_error_decorator
async def delete_user(
    user_id: Annotated[int, Path(ge=1)],
    current_user: Annotated[User, Depends(check_user_is_admin)],
    user_service: Annotated["UserService", Depends(UserService)],
):
    await user_service.delete(user_id=user_id)
    return
