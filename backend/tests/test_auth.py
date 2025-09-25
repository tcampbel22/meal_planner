AUTH_URL = "/api/auth/"
USER_URL = "/api/users/"


class TestAuthentication:
    def test_login_user(self, client):
        users = client.get(USER_URL)
        email = users.json()[0]["email"]
        password = "12345"
        print(f"DEBUG: {email} {password}")
        res = client.post(
            f"{AUTH_URL}login/", json={"email": email, "password": password}
        )
        assert res.status_code == 200
        assert res.json() == {
            "id": users.json()[0]["id"],
            "email": users.json()[0]["email"],
            "username": users.json()[0]["username"],
            "created_date": users.json()[0]["created_date"],
        }

    def test_missing_password(self, client):
        res = client.post(f"{AUTH_URL}login/", json={"email": "bob@hello.fi"})
        assert res.status_code == 422

    def test_missing_email(self, client):
        res = client.post(f"{AUTH_URL}login/", json={"password": "12345"})
        assert res.status_code == 422

    def test_user_not_found(self, client):
        res = client.post(
            f"{AUTH_URL}login/",
            json={"email": "zob@hello.fi", "password": "12345"},
        )
        assert res.status_code == 404

    def test_incorrect_password(self, client):
        res = client.post(
            f"{AUTH_URL}login/",
            json={"email": "bob@hello.fi", "password": "12345545456"},
        )
        assert res.status_code == 401
        assert res.json() == {"detail": "Invalid password or email"}

    def test_invalid_password(self, client):
        res = client.post(
            f"{AUTH_URL}login/",
            json={"email": "bob@hello.fi", "password": "12"},
        )
        assert res.status_code == 422

    def test_invalid_email(self, client):
        res = client.post(
            f"{AUTH_URL}login/",
            json={"email": "bobhello.fi", "password": "12234"},
        )
        assert res.status_code == 422
