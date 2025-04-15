from src.api.decorators import handle_error_decorator
from src.api.users.auth_dependencies import check_user_is_active
from src.schemas.order_schemas import CreateOrderSchema
from src.services.order_service import OrderService
from fastapi import APIRouter, Depends
from src.core import settings, User
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
