USER_URL = "/api/users/"


class TestUserEndpoints:
    def test_read_users(self, client):
        res = client.get(USER_URL)
        assert res.status_code == 200
        assert len(res.json()) == 12

    def test_non_existing_user(self, client):
        non_existing_id = "52f7deb4-a907-4e4e-ada3-518f87a7e524"
        res = client.get(f"{USER_URL}{non_existing_id}")
        assert res.status_code == 404
        assert res.json() == {
            "detail": "User with 52f7deb4-a907-4e4e-ada3-518f87a7e524 not found"
        }

    def test_get_user(self, client):
        users = client.get(USER_URL)
        id = users.json()[0]["id"]
        date = users.json()[0]["created_date"]
        res = client.get(f"{USER_URL}{id}")
        assert res.status_code == 200
        assert res.json() == {
            "id": id,
            "username": "bob",
            "email": "bob@hello.fi",
            "created_date": date,
        }

    def test_invalid_email(self, client):
        res = client.post(
            USER_URL,
            json={
                "username": "test",
                "password": "Test123",
                "email": "testtest.com",
            },
        )
        assert res.status_code == 422

    def test_missing_username(self, client):
        res = client.post(
            USER_URL, json={"password": "Test123", "email": "test@test.com"}
        )
        assert res.status_code == 422

    def test_missing_passsword(self, client):
        res = client.post(
            USER_URL, json={"username": "test", "email": "test@test.com"}
        )
        assert res.status_code == 422

    def test_missing_email(self, client):
        res = client.post(
            USER_URL, json={"username": "test", "password": "Test123"}
        )
        assert res.status_code == 422

    def test_add_user(self, client):
        res = client.post(
            USER_URL,
            json={
                "username": "Test",
                "password": "Test123",
                "email": "test@test.com",
            },
        )
        body = res.json()
        id = body["id"]
        date = body["created_date"]
        assert res.status_code == 201
        assert res.json() == {
            "id": id,
            "username": "Test",
            "email": "test@test.com",
            "created_date": date,
        }
        total = client.get(USER_URL)
        assert len(total.json()) == 13
        res = client.delete(f"{USER_URL}{id}")
        assert res.status_code == 204
        total = client.get(USER_URL)
        assert len(total.json()) == 12

    def test_delete_non_existing_user(self, client):
        total = client.get(USER_URL)
        assert len(total.json()) == 12
        non_existing_id = "52f7deb4-a907-4e4e-ada3-518f87a7e524"
        res = client.delete(f"{USER_URL}{non_existing_id}")
        assert res.status_code == 404
        total = client.get(USER_URL)
        assert len(total.json()) == 12

    def test_delete_user(self, client):
        total = client.get(USER_URL)
        assert len(total.json()) == 12
        id = total.json()[0]["id"]
        res = client.delete(f"{USER_URL}{id}")
        assert res.status_code == 204
        total = client.get(USER_URL)
        assert len(total.json()) == 11
