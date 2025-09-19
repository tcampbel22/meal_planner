import pytest
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from app.database.database import get_session
from fastapi.testclient import TestClient
from app.main import app
from app.database.models import Users  # noqa: F401

load_dotenv(".env.test")
DATABASE_URL = os.getenv("TEST_DB_URL")
engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def create_db_tables():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="session", autouse=True)
def create_users():
    with Session(engine) as session:
        from seed_db import seed_users

        users = seed_users(session)
        yield users


@pytest.fixture(scope="function")
def session():
    with Session(engine) as s:
        yield s
        s.rollback()


@pytest.fixture()
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
