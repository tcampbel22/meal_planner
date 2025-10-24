from pydantic import BaseModel
from typing import Optional
import uuid
import datetime
from app.api.schemas.recipe_schemas import RecipeOut


class MealPlanBase(BaseModel):
    id: uuid.UUID
    created_date: datetime.datetime
    recipes: list[RecipeOut] = []
    length: Optional[int] = 7


class MealPlanOut(MealPlanBase):
    user_id: uuid.UUID
