from pydantic import BaseModel, Field, EmailStr
import uuid
import datetime


class NewUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=5)


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    created_date: datetime.datetime
