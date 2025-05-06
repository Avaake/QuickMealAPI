from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from typing import Callable, Awaitable
from fastapi import Request, Response
from core import settings, Logger
import asyncio
import time

log = Logger(__name__).get_logger()
CallNext = Callable[[Request], Awaitable[Response]]


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: CallNext,
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.5f}"
        return response


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, timeout: int):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next: CallNext) -> Response:
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return ORJSONResponse(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                content={"detail": f"The request time exceeded {self.timeout} seconds"},
            )


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_middleware_request(
        request: Request,
        call_next: CallNext,
    ):
        log.info("Request %s to %s", request.method, request.url.path)
        return await call_next(request)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.midd.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(ProcessTimeHeaderMiddleware)
    app.add_middleware(
        TimeoutMiddleware,
        timeout=5,
    )
