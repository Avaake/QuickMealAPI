from src.schemas.base_schema import BaseSchema
from typing import Annotated, Optional, Self
from pydantic import (
    Field,
    model_validator,
    EmailStr,
    field_validator,
)
import re


class UserBaseSchema(BaseSchema):
    first_name: Annotated[
        str, Field(min_length=4, max_length=50, description="First name user")
    ]
    email: EmailStr
    phone_number: Annotated[
        str, Field(min_length=5, max_length=20, description="Phone number")
    ]

    @staticmethod
    @field_validator("phone_number")
    def validate_phone_number(value: str):
        if not re.match(r"^\+\d{5,15}$", value):
            raise ValueError("Phone number must be entered in the format: +999999999")
        return value


class CreateUserSchema(UserBaseSchema):
    last_name: Annotated[
        Optional[str], Field(max_length=50, description="last name user")
    ] = None
    password: Annotated[str, Field(min_length=4, description="Password user")]

    # @model_validator(mode="after")
    # def validate_password(self) -> Self:
    #     self.password = user_service.hash_password(self.password)
    #     return self


class ReadUserSchema(UserBaseSchema):
    id: int
    last_name: str | None
    is_active: bool
    is_user: bool
    is_admin: bool
    is_courier: bool


class LoginSchema(BaseSchema):
    email: EmailStr
    password: str


class TokenInfo(BaseSchema):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
