from fastapi import APIRouter, Depends, Path
from src.core import settings, Category
from src.schemas.category_schema import (
    CategoryBaseSchema,
    UpdateCategorySchema,
    ReadCategorySchema,
)
from src.services.category_service import CategoryService
from typing import Annotated

router = APIRouter(
    prefix=settings.api_prefix.categories,
    tags=["Categories"],
)


@router.post("", status_code=201, summary="Create a new category")
async def create_category(
    category_data: CategoryBaseSchema,
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> ReadCategorySchema:
    pass


@router.get("", status_code=200, summary="Get all categories")
async def get_all_categories(
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> list[ReadCategorySchema]:
    pass


@router.get("/{category_id}", summary="Get category")
async def get_category(
    category_id: int,
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> ReadCategorySchema:
    pass


@router.patch("/{category_id}", summary="Update category")
async def update_category(
    category_id: int,
    category_data: UpdateCategorySchema,
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> ReadCategorySchema:
    pass


@router.delete("/{category_id}", summary="Delete category")
async def delete_category(
    category_id: int,
    category_service: Annotated["CategoryService", Depends(CategoryService)],
):
    pass
