from fastapi import APIRouter
from core import settings
from api.users.views import router as users_router
from api.categories.views import router as categories_router
from api.dishes.views import router as dish_router
from api.carts.views import router as carts_router
from api.order.views import router as order_router


api_router = APIRouter(prefix=settings.api_prefix.api_v1)
api_router.include_router(users_router)
api_router.include_router(categories_router)
api_router.include_router(dish_router)
api_router.include_router(carts_router)
api_router.include_router(order_router)
