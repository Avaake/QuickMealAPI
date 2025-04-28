from api.users.auth_dependencies import check_user_is_admin
from api.decorators import handle_error_decorator
from services.dish_service import DishService
from fastapi import APIRouter, Depends, Query
from typing import Sequence, Annotated
from core import settings, User
from schemas.dish_schema import (
    DishBaseSchema,
    ReadDishSchema,
    UpdateDishSchema,
    QueryDishSchema,
)

router = APIRouter(prefix=settings.api_prefix.dishes, tags=["dishes"])


@router.post("", status_code=201, summary="create dish")
@handle_error_decorator
async def create_dish(
    dish_data: DishBaseSchema,
    current_user: Annotated[User, Depends(check_user_is_admin)],
    dish_service: Annotated["DishService", Depends(DishService)],
) -> ReadDishSchema:
    dish = await dish_service.add(dish_data)
    return ReadDishSchema(**dish.to_dict())


@router.get("", status_code=200, summary="get all dishes")
@handle_error_decorator
async def get_all_dishes(
    q: Annotated[QueryDishSchema, Query()],
    dish_service: Annotated["DishService", Depends(DishService)],
) -> Sequence[ReadDishSchema] | ReadDishSchema:
    dishes = await dish_service.get_all(category_id=q.category_id, order_by=q.order_by)
    return dishes


@router.get("/{dish_id}", status_code=200, summary="get dish")
@handle_error_decorator
async def get_dish(
    dish_id: int,
    dish_service: Annotated["DishService", Depends(DishService)],
) -> ReadDishSchema:
    dish = await dish_service.get(id=dish_id)
    return ReadDishSchema(**dish.to_dict())


@router.patch("/{dish_id}", status_code=200, summary="update dish")
@handle_error_decorator
async def update_dish(
    dish_id: int,
    dish_data: UpdateDishSchema,
    current_user: Annotated[User, Depends(check_user_is_admin)],
    dish_service: Annotated["DishService", Depends(DishService)],
) -> ReadDishSchema:
    dish = await dish_service.update(dish_id=dish_id, dish_data=dish_data)
    return ReadDishSchema(**dish.to_dict())


@router.delete("/{dish_id}", status_code=204, summary="delete dish")
@handle_error_decorator
async def delete_dish(
    dish_id: int,
    current_user: Annotated[User, Depends(check_user_is_admin)],
    dish_service: Annotated["DishService", Depends(DishService)],
) -> None:
    await dish_service.delete(dish_id=dish_id)
    return
