AUTH_URL = "/api/auth/"
USER_URL = "/api/users/"


class TestAuth:
    def test_login_user(self, client, create_one_user):
        email = "bob@hello.fi"
        password = "12345"

        res = client.post(
            f"{AUTH_URL}token",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 200
        assert "access_token" in res.json()
        assert res.json()["token_type"] == "bearer"

    def test_logout_user(self, client, auth_headers, create_one_user):
        email = "bob@hello.fi"
        password = "12345"

        res = client.post(
            f"{AUTH_URL}token",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 200
        assert "access_token" in res.json()
        assert res.json()["token_type"] == "bearer"

        res = client.post(f"{AUTH_URL}logout", headers=auth_headers)
        assert res.status_code == 200
        assert res.json() == {"message": "User bob logged out"}

    def test_missing_password(self, client, create_one_user):
        res = client.post(
            f"{AUTH_URL}token",
            data={"username": "bob@hello.fi"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 422

    def test_missing_email(self, client, create_one_user):
        res = client.post(
            f"{AUTH_URL}token",
            data={"password": "12345"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 422

    def test_user_not_found(self, client, create_one_user):
        res = client.post(
            f"{AUTH_URL}token",
            data={"username": "zob@hello.fi", "password": "12345"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 404

    def test_incorrect_password(self, client, create_one_user):
        res = client.post(
            f"{AUTH_URL}token",
            data={"username": "bob@hello.fi", "password": "12345545456"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 401
        assert res.json() == {
            "headers": {"WWW-Authenticate": "Bearer"},
            "detail": "Invalid password or email",
        }

    def test_invalid_password(self, client, create_one_user):
        res = client.post(
            f"{AUTH_URL}token",
            data={"username": "bob@hello.fi", "password": "12"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 422

    def test_invalid_email(self, client, create_one_user):
        res = client.post(
            f"{AUTH_URL}token",
            data={"username": "bobhello.fi", "password": "12234"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 422

    def test_expired_token(
        self, client, monkeypatch, auth_headers, create_one_user
    ):
        from jwt.exceptions import ExpiredSignatureError
        import jwt

        def mock_decode(*args, **kwargs):
            raise ExpiredSignatureError()

        monkeypatch.setattr(jwt, "decode", mock_decode)

        res = client.get(USER_URL, headers=auth_headers)
        assert res.status_code == 401
        assert res.json() == {
            "headers": {"WWW-Authenticate": "Bearer"},
            "detail": "Token is expired",
        }
