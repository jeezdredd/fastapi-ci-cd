from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


# ==== Ingredient ====
class IngredientBase(BaseModel):
    name: str = Field(..., description="Название ингредиента")
    amount: str = Field(..., description="Количество/вес, напр.: '200 г' или '1 ч.л.'")


class IngredientCreate(IngredientBase):
    pass


class IngredientOut(IngredientBase):
    id: int = Field(..., description="ID ингредиента")

    model_config = {"from_attributes": True}


# ==== Recipe ====
class RecipeBase(BaseModel):
    name: str = Field(..., description="Название блюда")
    time_minutes: int = Field(..., ge=1, description="Время приготовления, минуты")
    description: str = Field(..., description="Текстовое описание рецепта")


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate] = Field(
        default_factory=list, description="Список ингредиентов"
    )


class RecipeListItem(BaseModel):
    id: int
    name: str
    time_minutes: int
    views_count: int

    model_config = {"from_attributes": True}


class RecipeDetail(BaseModel):
    id: int
    name: str
    time_minutes: int
    description: str
    views_count: int
    ingredients: List[IngredientOut]

    model_config = {"from_attributes": True}
