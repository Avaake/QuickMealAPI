from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import DatabaseError
from core import Logger
from exceptions import NotFoundError, AlreadyExistsError

log = Logger(__name__).get_logger()


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
    def connection_error_handler(
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

    @app.exception_handler(NotFoundError)
    def not_found_error_handler(
        request: Request,
        exc: NotFoundError,
    ) -> ORJSONResponse:
        log.info("Not found: %s", str(exc))
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(AlreadyExistsError)
    def already_exists_error_handler(
        request: Request,
        exc: AlreadyExistsError,
    ):
        log.info("Already exists: %s", str(exc))
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": str(exc),
            },
        )
