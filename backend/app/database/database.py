import os
import dotenv
from pathlib import Path
from fastapi import Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")
DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        print("Databases created successfully")
    except Exception as e:
        print(f"Failed to create databases: {e}")


def shutdown():
    engine.dispose()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
