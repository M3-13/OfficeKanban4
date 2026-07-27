def test_register_and_login(client):
    r = client.post("/auth/register", json={"username": "testuser", "password": "secret123"})
    assert r.status_code == 201
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    r2 = client.post("/auth/login", json={"username": "testuser", "password": "secret123"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()


def test_register_duplicate_username(client):
    client.post("/auth/register", json={"username": "dup", "password": "secret123"})
    r = client.post("/auth/register", json={"username": "dup", "password": "secret123"})
    assert r.status_code == 409


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "user1", "password": "secret123"})
    r = client.post("/auth/login", json={"username": "user1", "password": "wrong"})
    assert r.status_code == 401


def test_login_nonexistent_user(client):
    r = client.post("/auth/login", json={"username": "nobody", "password": "secret123"})
    assert r.status_code == 401


def test_me_endpoint(client):
    r = client.post("/auth/register", json={"username": "me_user", "password": "secret123"})
    token = r.json()["access_token"]
    r2 = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["username"] == "me_user"


def test_me_without_token(client):
    r = client.get("/auth/me")
    assert r.status_code == 401


def test_me_with_invalid_token(client):
    r = client.get("/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert r.status_code == 401


def test_validation_username_too_short(client):
    r = client.post("/auth/register", json={"username": "ab", "password": "secret123"})
    assert r.status_code == 422


def test_validation_password_too_short(client):
    r = client.post("/auth/register", json={"username": "validuser", "password": "12345"})
    assert r.status_code == 422


def test_protected_endpoint_requires_auth(client):
    r = client.get("/boards")
    assert r.status_code == 401


def test_protected_endpoint_with_token_returns_200(client):
    r = client.post("/auth/register", json={"username": "board_user", "password": "secret123"})
    token = r.json()["access_token"]
    r2 = client.get("/boards", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
