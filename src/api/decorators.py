from fastapi import HTTPException, status
from functools import wraps
from exceptions import (
    CategoryAlreadyExistsError,
    UserAlreadyExistsError,
    TokenIsNotValidError,
    ServiceError,
    NotFoundError,
)


def handle_error_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (
            CategoryAlreadyExistsError,
            TokenIsNotValidError,
            UserAlreadyExistsError,
            ServiceError,
            NotFoundError,
        ) as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
            )

    return wrapper
