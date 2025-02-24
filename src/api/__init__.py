from fastapi import APIRouter
from src.core import settings
from src.api.users.views import router as users_router


api_router = APIRouter(prefix=settings.api_prefix.api_v1)
api_router.include_router(users_router)
