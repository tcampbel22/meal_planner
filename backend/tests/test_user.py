from utils import delete_user, get_users_length, get_all_users

USER_URL = "/api/users/"


class TestUserEndpoints:
    def test_read_users(self, client, auth_headers):
        res = client.get(USER_URL, headers=auth_headers)
        assert res.status_code == 200
        assert len(res.json()) == 12

    def test_non_existing_user(self, client, auth_headers):
        non_existing_id = "52f7deb4-a907-4e4e-ada3-518f87a7e524"
        res = client.get(f"{USER_URL}{non_existing_id}", headers=auth_headers)
        assert res.status_code == 404
        assert res.json() == {
            "detail": "User with 52f7deb4-a907-4e4e-ada3-518f87a7e524 not found"
        }

    def test_get_users_with_invalid_token(self, client):
        res = client.get(
            USER_URL, headers={"Authorization": "Bearer invalid_token"}
        )
        assert res.status_code == 401

    def test_get_user(self, client, auth_headers):
        users = client.get(USER_URL, headers=auth_headers)
        id = users.json()[0]["id"]
        date = users.json()[0]["created_date"]
        res = client.get(f"{USER_URL}{id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json() == {
            "id": id,
            "username": "bob",
            "email": "bob@hello.fi",
            "created_date": date,
            "recipes": [],
            "mealplans": [],
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

    def test_add_user(self, client, session):
        assert get_users_length(session) == 12

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
            "recipes": [],
            "mealplans": [],
        }

        assert get_users_length(session) == 13

        delete_user(id, session)
        assert get_users_length(session) == 12

    def test_delete_other_existing_user(self, client, auth_headers, session):
        assert get_users_length(session) == 12

        non_existing_id = "52f7deb4-a907-4e4e-ada3-518f87a7e524"
        res = client.delete(
            f"{USER_URL}{non_existing_id}", headers=auth_headers
        )
        assert res.status_code == 403
        assert get_users_length(session) == 12

    def test_delete_user(self, client, auth_headers, session):
        assert get_users_length(session) == 12
        users = get_all_users(session)
        id = users[0].id
        print(f"DEBUG: id-{id}, user: {users[0].username}")
        res = client.delete(f"{USER_URL}{id}", headers=auth_headers)
        assert res.status_code == 204
        assert get_users_length(session) == 11
