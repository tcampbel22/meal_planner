from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from typing import Optional
import uuid
import datetime


class RecipeBase(BaseModel):
    name: str = Field(alias="recipeName", min_length=3, max_length=30)
    url: Optional[AnyUrl] = Field(alias="recipeUrl", default=None)
    cuisine: Optional[str] = Field(max_length=20, default="-")
    default_portion: Optional[int] = Field(alias="portionSize", default=2)

    model_config = ConfigDict(populate_by_name=True)


class RecipeCreate(RecipeBase):
    user_id: uuid.UUID


class RecipeOut(RecipeBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_date: datetime.datetime
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
