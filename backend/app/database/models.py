from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from pydantic import EmailStr
from typing import Optional
from datetime import datetime, timezone
import uuid


class Users(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    email: EmailStr = Field(unique=True)
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    recipes: list["Recipes"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    mealplans: list["MealPlans"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class MealPlanRecipeLink(SQLModel, table=True):
    mealplan_id: uuid.UUID = Field(foreign_key="mealplans.id", primary_key=True)
    recipe_id: uuid.UUID = Field(foreign_key="recipes.id", primary_key=True)


class Recipes(SQLModel, table=True):
    __tablename__ = "recipes"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="unique_user_recipe_name"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    user: Users = Relationship(back_populates="recipes")
    url: Optional[str] = Field(default=None)
    name: str = Field(min_length=3, max_length=30)
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    cuisine: str = Field(min_length=3, max_length=20)
    default_portion: Optional[int] = Field(default=2)
    mealplans: list["MealPlans"] = Relationship(
        back_populates="recipes", link_model=MealPlanRecipeLink
    )


class MealPlans(SQLModel, table=True):
    __tablename__ = "mealplans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    user: "Users" = Relationship(back_populates="mealplans")
    recipes: list["Recipes"] = Relationship(
        back_populates="mealplans", link_model=MealPlanRecipeLink
    )
    length: int = Field(default=7)
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
