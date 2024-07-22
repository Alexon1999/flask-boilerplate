class TestUserView:
    def test_register_user(self, client):
        payload = {
            "username": "john",
            "email": "john@gmail.com",
            "password": "password",
        }
        res = client.post("/authentication/user/register", json=payload)
        assert res.status_code == 201
        assert res.json["username"] == payload["username"]

    def test_already_registered_username(self, client):
        payload = {
            "username": "john",
            "email": "john184@gmail.com",
            "password": "password",
        }

        res = client.post("/authentication/user/register", json=payload)
        assert res.status_code == 400
        assert res.json["message"] == "User already exists"

    def test_already_registered_email(self, client):
        payload = {
            "username": "john184",
            "email": "john@gmail.com",
            "password": "password",
        }

        res = client.post("/authentication/user/register", json=payload)
        assert res.status_code == 400
        assert res.json["message"] == "User already exists"

    def test_login_user(self, client):
        payload = {
            "email": "john@gmail.com",
            "password": "password",
        }

        res = client.post("/authentication/login", json=payload)
        assert res.status_code == 200
        assert len(res.json["access_token"]) > 0
        assert len(res.json["refresh_token"]) > 0

    def test_login_user_invalid_credentials_email(self, client):
        payload = {
            "email": "john123@gmail.com",
            "password": "password",
        }
        res = client.post("/authentication/login", json=payload)
        assert res.status_code == 401
        assert res.json["message"] == "Invalid email or password"

    def test_login_user_invalid_credentials_password(self, client):
        payload = {
            "email": "john@gmail.com",
            "password": "password123",
        }
        res = client.post("/authentication/login", json=payload)
        assert res.status_code == 401
        assert res.json["message"] == "Invalid email or password"

    def test_refresh_token(self, client):
        payload = {
            "email": "john@gmail.com",
            "password": "password",
        }
        res = client.post("/authentication/login", json=payload)
        assert res.status_code == 200
        refresh_token = res.json["refresh_token"]

        headers = {
            "Authorization": f"Bearer {refresh_token}",
        }
        res = client.post("/authentication/refresh", headers=headers)
        assert res.status_code == 200
        assert len(res.json["access_token"]) > 0

    def test_refresh_token(self, client):
        refresh_token = "invalid_refresh_token"

        headers = {
            "Authorization": f"Bearer {refresh_token}",
        }
        res = client.post("/authentication/refresh", headers=headers)
        assert res.status_code == 422

    def test_protected_route(self, client):
        payload = {
            "email": "john@gmail.com",
            "password": "password",
        }
        res = client.post("/authentication/login", json=payload)
        assert res.status_code == 200
        access_token = res.json["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        res = client.get("/authentication/protected", headers=headers)
        assert res.status_code == 200

    def test_protected_route(self, client):
        access_token = "invalid_access_token"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        res = client.get("/authentication/protected", headers=headers)
        assert res.status_code == 422
