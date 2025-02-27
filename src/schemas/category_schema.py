from src.schemas.base_schema import BaseSchema
from typing import Annotated, Optional
from pydantic import Field


class CategoryBaseSchema(BaseSchema):
    name: Annotated[str, Field(min_length=5, description="Category name")]
    description: Annotated[
        Optional[str], Field(min_length=10, description="Category description")
    ] = None


class ReadCategorySchema(CategoryBaseSchema):
    id: int


class UpdateCategorySchema(BaseSchema):
    name: Annotated[Optional[str], Field(min_length=5, description="Category name")] = (
        None
    )
