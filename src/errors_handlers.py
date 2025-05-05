from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import DatabaseError
from core import log


def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(DatabaseError)
    def db_error_handler(
        request: Request,
        exc: DatabaseError,
    ) -> ORJSONResponse:
        log.error("Database error:", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "There was an unforeseen error. Our administrators are already working on it."
            },
        )

    @app.exception_handler(ConnectionRefusedError)
    def db_error_handler(
        request: Request,
        exc: DatabaseError,
    ) -> ORJSONResponse:
        log.error("Connection error:", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "There was an unforeseen error. Our administrators are already working on it."
            },
        )
