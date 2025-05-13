from schemas.order_schemas import (
    CreateOrderSchema,
    UpdateOrderSchema,
    ReadOrderSchema,
)
from api.users.auth_dependencies import (
    check_user_is_courier_or_is_admin,
    check_user_is_active,
)
from services.order_service import OrderService
from fastapi import APIRouter, Depends, Path
from core import settings, User, Logger
from typing import Annotated

log = Logger(__name__).get_logger()
router = APIRouter(prefix=settings.api_prefix.orders, tags=["Order"])


@router.post("", status_code=201, response_model=ReadOrderSchema)
async def create_order(
    order_data: CreateOrderSchema,
    current_user: Annotated[User, Depends(check_user_is_active)],
    order_service: Annotated["OrderService", Depends(OrderService)],
):
    order = await order_service.add(user_id=current_user.id, data=order_data)
    return ReadOrderSchema.model_validate(order).model_dump()


@router.put("/{order_id}", status_code=200)
async def update_order_status(
    order_id: Annotated[int, Path(ge=1)],
    order_data: UpdateOrderSchema,
    current_user: Annotated[User, Depends(check_user_is_courier_or_is_admin)],
    order_service: Annotated["OrderService", Depends(OrderService)],
):
    order = order_service.update(order_data=order_data, order_id=order_id)
