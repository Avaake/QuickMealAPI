from api.users.auth_dependencies import check_user_is_admin
from services.category_service import CategoryService
from fastapi import APIRouter, Depends, Path
from schemas.category_schema import (
    CategoryBaseSchema,
    UpdateCategorySchema,
    ReadCategorySchema,
)
from typing import Annotated, Sequence
from core import settings, User


router = APIRouter(
    prefix=settings.api_prefix.categories,
    tags=["Categories"],
)


@router.post(
    "",
    status_code=201,
    summary="Create a new category",
    response_model_exclude_none=True,
)
async def create_category(
    category_data: CategoryBaseSchema,
    current_user: Annotated[User, Depends(check_user_is_admin)],
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> ReadCategorySchema:
    category = await category_service.add(category_data=category_data)
    return ReadCategorySchema(**category.to_dict())


@router.get(
    "",
    response_model=Sequence[ReadCategorySchema],
    status_code=200,
    summary="Get all categories",
)
async def get_all_categories(
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> Sequence[ReadCategorySchema]:
    categories = await category_service.get_all()
    return categories


@router.get("/{category_id}", summary="Get category")
async def get_category(
    category_id: Annotated[int, Path(ge=1)],
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> ReadCategorySchema:
    category = await category_service.get(id=category_id)
    return ReadCategorySchema(**category.to_dict())


@router.patch("/{category_id}", summary="Update category")
async def update_category(
    category_id: Annotated[int, Path(ge=1)],
    category_data: UpdateCategorySchema,
    current_user: Annotated[User, Depends(check_user_is_admin)],
    category_service: Annotated["CategoryService", Depends(CategoryService)],
) -> ReadCategorySchema:
    category = await category_service.update(
        category_id=category_id, category_data=category_data
    )
    return ReadCategorySchema(**category.to_dict())


@router.delete("/{category_id}", summary="Delete category", status_code=204)
async def delete_category(
    category_id: Annotated[int, Path(ge=1)],
    current_user: Annotated[User, Depends(check_user_is_admin)],
    category_service: Annotated["CategoryService", Depends(CategoryService)],
):
    await category_service.delete(category_id=category_id)
    return
