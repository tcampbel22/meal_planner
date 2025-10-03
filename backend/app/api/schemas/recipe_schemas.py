from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from typing import Optional
import uuid
import datetime


class RecipeBase(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    url: Optional[AnyUrl] = None
    cuisine: str = Field(min_length=3, max_length=20)
    default_portion: Optional[int] = 2


class RecipeCreate(RecipeBase):
    user_id: uuid.UUID


class RecipeOut(RecipeBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_date: datetime.datetime
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
