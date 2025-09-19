from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""BASIC TESTS
	Tests for incorrect endpoints, connections etc
"""


def test_invalid_endpoint():
    res = client.get("/fake")
    assert res.status_code == 404
