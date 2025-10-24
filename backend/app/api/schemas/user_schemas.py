from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.api.schemas.recipe_schemas import RecipeOut
from app.api.schemas.mealplan_schemas import MealPlanOut
import uuid
import datetime


class BaseUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr


class UserOut(BaseUser):
    id: uuid.UUID
    created_date: datetime.datetime
    recipes: list[RecipeOut] = []
    mealplans: list[MealPlanOut] = []


class AuthUser(BaseUser):
    username: Optional[str] = None
    password: str = Field(min_length=5)
