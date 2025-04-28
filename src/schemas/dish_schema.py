from schemas.base_schema import BaseSchema
from typing import Annotated, Optional
from pydantic import Field


class DishBaseSchema(BaseSchema):
    name: Annotated[str, Field(min_length=3, description="Dish name")]
    description: Annotated[
        Optional[str], Field(min_length=10, description="dishes description")
    ] = None
    price: Annotated[int, Field(gt=0, description="dishes price")]
    category_id: Annotated[
        int, Field(gt=0, description="id of which category the dishes belongs to")
    ]


class ReadDishSchema(DishBaseSchema):
    id: int


class UpdateDishSchema(DishBaseSchema):
    name: Annotated[Optional[str], Field(min_length=3, description="Dish name")] = None
    price: Annotated[Optional[int], Field(gt=0, description="dishes price")] = None
    category_id: Annotated[
        Optional[int],
        Field(gt=0, description="id of which category the dishes belongs to"),
    ] = None


class QueryDishSchema(BaseSchema):
    category_id: Annotated[
        Optional[int],
        Field(ge=1, description="id of which category the dishes belongs to"),
    ] = None
    order_by: Annotated[Optional[bool], Field()] = False
