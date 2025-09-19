from pydantic import BaseModel, Field, EmailStr
import uuid
import datetime


class BaseUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr


class UserOut(BaseUser):
    id: uuid.UUID
    created_date: datetime.datetime


class NewUser(BaseUser):
    password: str = Field(min_length=5)
