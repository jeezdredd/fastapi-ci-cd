from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas


def create_recipe(db: Session, data: schemas.RecipeCreate) -> models.Recipe:
    recipe = models.Recipe(
        name=data.name,
        time_minutes=data.time_minutes,
        description=data.description,
    )
    for ing in data.ingredients:
        recipe.ingredients.append(models.Ingredient(name=ing.name, amount=ing.amount))

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


def list_recipes(db: Session, limit: int = 100, offset: int = 0) -> List[models.Recipe]:
    stmt = (
        select(models.Recipe)
        .order_by(models.Recipe.views_count.desc(), models.Recipe.time_minutes.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(stmt).scalars())


def get_recipe_and_increment_views(db: Session, recipe_id: int) -> models.Recipe | None:
    recipe = db.get(models.Recipe, recipe_id)
    if recipe is None:
        return None
    recipe.views_count += 1
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe
