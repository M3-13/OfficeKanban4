import os
import tempfile

import pytest
from fastapi.testclient import TestClient

os.environ["JWT_SECRET"] = "test-secret-key-for-pytest"
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(
    tempfile.gettempdir(), "test_officekanban.db"
)

from backend.database import Base, engine
from backend.main import app


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def _register_and_get_token(client, username):
    r = client.post("/auth/register", json={"username": username, "password": "secret123"})
    return r.json()["access_token"]


@pytest.fixture()
def auth_headers(client):
    token = _register_and_get_token(client, "testuser")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def auth_headers_other(client):
    token = _register_and_get_token(client, "otheruser")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def test_board(client, auth_headers):
    r = client.post("/boards", json={"title": "Test Board"}, headers=auth_headers)
    assert r.status_code == 201, f"Board creation failed: {r.json()}"
    return r.json()


@pytest.fixture()
def test_column(client, auth_headers, test_board):
    r = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "Test Column"},
        headers=auth_headers,
    )
    assert r.status_code == 201, f"Column creation failed: {r.json()}"
    return r.json()
