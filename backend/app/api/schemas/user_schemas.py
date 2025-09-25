from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid
import datetime


class BaseUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr


class UserOut(BaseUser):
    id: uuid.UUID
    created_date: datetime.datetime


class AuthUser(BaseUser):
    username: Optional[str] = None
    password: str = Field(min_length=5)
