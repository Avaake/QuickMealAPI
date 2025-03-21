from src.api.users.auth_dependencies import check_user_is_active
from src.api.decorators import handle_error_decorator
from src.services.cart_service import CartService
from fastapi import APIRouter, Depends, Path
from typing import Sequence, Annotated
from src.schemas.cart_schemas import (
    BaseCartSchema,
    ReadCartDishSchema,
)
from src.core import settings, User


router = APIRouter(prefix=settings.api_prefix.carts, tags=["Cart | Basket"])


@router.post("/add", status_code=201)
@handle_error_decorator
async def add_to_cart(
    cart_data: BaseCartSchema,
    current_user: Annotated[User, Depends(check_user_is_active)],
    cart_service: Annotated["CartService", Depends(CartService)],
) -> dict[str, str]:
    await cart_service.add(user_id=current_user.id, cart_data=cart_data)
    return {"message": "Dish added to cart."}


@router.get("/total-price", status_code=200)
@handle_error_decorator
async def get_total(
    current_user: Annotated[User, Depends(check_user_is_active)],
    cart_service: Annotated["CartService", Depends(CartService)],
) -> dict[str, int]:
    total_price = await cart_service.calculate_total(user_id=current_user.id)
    return {"total_price": total_price}


@router.get("", status_code=200)
@handle_error_decorator
async def get_cart(
    current_user: Annotated[User, Depends(check_user_is_active)],
    cart_service: Annotated["CartService", Depends(CartService)],
) -> Sequence[ReadCartDishSchema] | ReadCartDishSchema:
    cart = await cart_service.get(user_id=current_user.id)
    return cart


@router.delete("/remove/{dish_id}")
@handle_error_decorator
async def remove_from_cart(
    dish_id: Annotated[int, Path(ge=1)],
    current_user: Annotated[User, Depends(check_user_is_active)],
    cart_service: Annotated["CartService", Depends(CartService)],
) -> dict[str, str]:
    await cart_service.update(user_id=current_user.id, dish_id=dish_id)
    return {"message": "Dish removed from cart."}


@router.delete("", status_code=204)
@handle_error_decorator
async def clear_cart(
    current_user: Annotated[User, Depends(check_user_is_active)],
    cart_service: Annotated["CartService", Depends(CartService)],
) -> None:
    await cart_service.delete(user_id=current_user.id)
    return
