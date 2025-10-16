from __future__ import annotations
from typing import List
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    time_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)

    ingredients: Mapped[List["Ingredient"]] = relationship(
        "Ingredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[str] = mapped_column(String(255), nullable=False)

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="ingredients")
