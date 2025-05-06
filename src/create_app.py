from typing import AsyncGenerator
from contextlib import asynccontextmanager
from core import db_helper
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.errors_handlers import register_error_handlers
from core.middlewares import register_middleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="QuickMealAPI",
        default_response_class=ORJSONResponse,
    )

    register_error_handlers(app=app)
    register_middleware(app=app)

    return app
