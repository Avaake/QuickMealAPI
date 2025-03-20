from src.schemas.base_schema import BaseSchema
from typing import Annotated, Optional
from pydantic import (
    Field,
)


class BaseCartSchema(BaseSchema):
    dish_id: Annotated[int, Field(ge=0, description="id of dish")]
    quantity: Annotated[int, Field(ge=0, description="quantity of item")]


class ReadCartSchema(BaseCartSchema):
    id: int


class UpdateCartSchema(BaseCartSchema):
    dish_id: Annotated[Optional[int], Field(ge=0, description="id of dish")] = None
    quantity: Annotated[Optional[int], Field(ge=0, description="quantity of item")] = (
        None
    )


class CreateCartSchema(BaseCartSchema):
    user_id: int


class ReadCartDishSchema(BaseCartSchema):
    name: str
