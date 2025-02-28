from fastapi import HTTPException, status


class ServiceError(Exception):
    pass


class TokenIsNotValidError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class CategoryAlreadyExistsError(Exception):
    pass


class NotFoundError(Exception):
    pass


UNAUTHORIZED_EXC_INCORRECT = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
)

FORBIDDEN_EXC_INACTIVE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="inactive user",
)

TOKEN_INVALID_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"invalid token",
)


FORBIDDEN_EXC_NOT_ENOUGH_RIGHTS = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough rights",
)
