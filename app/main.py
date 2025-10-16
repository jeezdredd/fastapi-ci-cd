from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import engine, get_db
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Кулинарная книга API",
    version="1.0.0",
    description=(
        "API для списка и детальных карточек рецептов.\n\n"
        "* Список рецептов отсортирован по популярности (views_count) и времени готовки.\n"
        "* При открытии детальной карточки счётчик просмотров увеличивается."
    ),
    contact={"name": "Backend Team", "email": "backend@example.com"},
)


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeListItem],
    summary="Список всех рецептов",
    tags=["Recipes"],
)
def get_recipes(
    limit: int = Query(100, ge=1, le=500, description="Сколько записей вернуть"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    db: Session = Depends(get_db),
):
    items = crud.list_recipes(db, limit=limit, offset=offset)
    return items


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    summary="Детальная карточка рецепта (увеличивает просмотры)",
    tags=["Recipes"],
)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.get_recipe_and_increment_views(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.post(
    "/recipes",
    response_model=schemas.RecipeDetail,
    status_code=201,
    summary="Создать новый рецепт",
    tags=["Recipes"],
)
def create_recipe(payload: schemas.RecipeCreate, db: Session = Depends(get_db)):
    from sqlalchemy import select

    from .models import Recipe

    exists = db.execute(
        select(Recipe).where(Recipe.name == payload.name)
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(
            status_code=409, detail="Recipe with this name already exists"
        )

    recipe = crud.create_recipe(db, payload)
    return recipe
