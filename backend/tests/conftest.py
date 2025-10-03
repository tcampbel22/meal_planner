import pytest
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session
from app.database.database import get_session, get_engine
from fastapi.testclient import TestClient
from app.main import app
from app.database.models import Users  # noqa: F401

os.environ["ENV"] = "test"

load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.test")
)

engine = get_engine()


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


@pytest.fixture()
def auth_headers(client):
    res = client.post(
        "/api/auth/token",
        data={"username": "bob@hello.fi", "password": "12345"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


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
