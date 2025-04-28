from schemas.order_schemas import CreateOrderSchema, UpdateOrderSchema
from api.users.auth_dependencies import (
    check_user_is_courier_or_is_admin,
    check_user_is_active,
)
from api.decorators import handle_error_decorator
from services.order_service import OrderService
from fastapi import APIRouter, Depends, Path
from core import settings, User
from typing import Annotated


router = APIRouter(prefix=settings.api_prefix.orders, tags=["Order"])


@router.post("", status_code=201)
@handle_error_decorator
async def create_order(
    order_data: CreateOrderSchema,
    current_user: Annotated[User, Depends(check_user_is_active)],
    order_service: Annotated["OrderService", Depends(OrderService)],
) -> dict:
    await order_service.add(user_id=current_user.id, data=order_data)
    return {"success": True}


@router.put("/{order_id}", status_code=200)
@handle_error_decorator
async def update_order_status(
    order_id: Annotated[int, Path(ge=1)],
    order_data: UpdateOrderSchema,
    current_user: Annotated[User, Depends(check_user_is_courier_or_is_admin)],
    order_service: Annotated["OrderService", Depends(OrderService)],
):
    order = order_service.update(order_data=order_data, order_id=order_id)
