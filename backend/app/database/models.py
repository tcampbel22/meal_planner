from sqlmodel import SQLModel, Field, Relationship, Column, LargeBinary
from pydantic import EmailStr
from typing import Optional
from datetime import datetime, timezone
import uuid


class Users(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: bytes = Field(sa_column=Column(LargeBinary, nullable=False))
    email: EmailStr = Field(unique=True)
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    recipes: list["Recipes"] = Relationship(back_populates="user")


class Recipes(SQLModel, table=True):
    __tablename__ = "recipes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    user: Users = Relationship(back_populates="recipes")
    url: Optional[str] = None
    name: str
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    default_portion: int = Field(default=2)
