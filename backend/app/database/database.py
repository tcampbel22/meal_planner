import os
import dotenv
import time
from pathlib import Path
from fastapi import Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")


def get_db_url():
    if os.getenv("ENV") == "test":
        return os.getenv("TEST_DB_URL")
    else:
        return os.getenv("DB_URL")


def get_engine(max_retries=5, delay=2):
    if not hasattr(get_engine, "engine") or get_engine.engine is None:
        url = get_db_url()
        if not url:
            raise ValueError("No db URL found")

        retries = 0
        while retries < max_retries:
            try:
                get_engine.engine = create_engine(url, echo=True)
                with get_engine.engine.connect():
                    pass
                return get_engine.engine
            except Exception as e:
                retries += 1
                if retries < max_retries:
                    print("INFO: Retrying connection")
                    time.sleep(delay)
                else:
                    print(f"INFO: Database connection failed: {e}")
                    raise RuntimeError(
                        f"Could not connect to database: {type(e).__name__}"
                    )
    print("INFO: Database connected")
    return get_engine.engine


def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(get_engine())
        print("Database created successfully")
    except Exception as e:
        print(f"Failed to create databases: {e}")


def shutdown():
    if hasattr(get_engine, "engine") and get_engine.engine:
        get_engine.engine.dispose()


def get_session():
    with Session(get_engine()) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
