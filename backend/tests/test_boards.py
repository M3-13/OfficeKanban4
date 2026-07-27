from fastapi.testclient import TestClient

from backend.database import SessionLocal
from backend.models import Column


def _register(client: TestClient, username: str, password: str = "secret123") -> str:
    r = client.post("/auth/register", json={"username": username, "password": password})
    assert r.status_code == 201
    return r.json()["access_token"]


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


class TestListBoards:
    def test_empty(self, client):
        token = _register(client, "user1")
        r = client.get("/boards", headers=_auth_header(token))
        assert r.status_code == 200
        assert r.json() == []

    def test_sorted_by_title(self, client):
        token = _register(client, "user2")
        for title in ["Zebra", "Alpha", "Beta"]:
            client.post("/boards", json={"title": title}, headers=_auth_header(token))
        r = client.get("/boards", headers=_auth_header(token))
        assert r.status_code == 200
        titles = [b["title"] for b in r.json()]
        assert titles == ["Alpha", "Beta", "Zebra"]

    def test_only_own_boards(self, client):
        t1 = _register(client, "owner1")
        t2 = _register(client, "owner2")
        client.post("/boards", json={"title": "Board A"}, headers=_auth_header(t1))
        client.post("/boards", json={"title": "Board B"}, headers=_auth_header(t2))
        r = client.get("/boards", headers=_auth_header(t1))
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        assert data[0]["title"] == "Board A"


class TestCreateBoard:
    def test_creates_with_default_columns(self, client):
        token = _register(client, "user3")
        r = client.post("/boards", json={"title": "My Board"}, headers=_auth_header(token))
        assert r.status_code == 201
        data = r.json()
        assert data["title"] == "My Board"
        assert data["owner_id"] is not None

        board_id = data["id"]
        db = SessionLocal()
        cols = db.query(Column).filter(Column.board_id == board_id).order_by(Column.position).all()
        db.close()
        assert len(cols) == 3
        titles_positions = [(c.title, c.position) for c in cols]
        assert titles_positions == [("To Do", 0), ("In Progress", 1), ("Done", 2)]

    def test_validation_title_too_long(self, client):
        token = _register(client, "user4")
        r = client.post("/boards", json={"title": "x" * 101}, headers=_auth_header(token))
        assert r.status_code == 422

    def test_validation_title_empty(self, client):
        token = _register(client, "user5")
        r = client.post("/boards", json={"title": ""}, headers=_auth_header(token))
        assert r.status_code == 422


class TestUpdateBoard:
    def test_rename_success(self, client):
        token = _register(client, "user6")
        r = client.post("/boards", json={"title": "Old Name"}, headers=_auth_header(token))
        board_id = r.json()["id"]
        r2 = client.put(
            f"/boards/{board_id}",
            json={"title": "New Name"},
            headers=_auth_header(token),
        )
        assert r2.status_code == 200
        assert r2.json()["title"] == "New Name"

    def test_not_found(self, client):
        token = _register(client, "user7")
        r = client.put("/boards/9999", json={"title": "X"}, headers=_auth_header(token))
        assert r.status_code == 404

    def test_wrong_owner_returns_404(self, client):
        t1 = _register(client, "owner_a")
        t2 = _register(client, "owner_b")
        r = client.post("/boards", json={"title": "Board"}, headers=_auth_header(t1))
        board_id = r.json()["id"]
        r2 = client.put(
            f"/boards/{board_id}",
            json={"title": "Hijack"},
            headers=_auth_header(t2),
        )
        assert r2.status_code == 404

    def test_validation_title_too_long(self, client):
        token = _register(client, "user8")
        r = client.post("/boards", json={"title": "Board"}, headers=_auth_header(token))
        board_id = r.json()["id"]
        r2 = client.put(
            f"/boards/{board_id}",
            json={"title": "x" * 101},
            headers=_auth_header(token),
        )
        assert r2.status_code == 422

    def test_validation_title_empty(self, client):
        token = _register(client, "user9")
        r = client.post("/boards", json={"title": "Board"}, headers=_auth_header(token))
        board_id = r.json()["id"]
        r2 = client.put(
            f"/boards/{board_id}",
            json={"title": ""},
            headers=_auth_header(token),
        )
        assert r2.status_code == 422


class TestDeleteBoard:
    def test_delete_success(self, client):
        token = _register(client, "user10")
        r = client.post("/boards", json={"title": "Gone"}, headers=_auth_header(token))
        board_id = r.json()["id"]
        r2 = client.delete(f"/boards/{board_id}", headers=_auth_header(token))
        assert r2.status_code == 204

        r3 = client.get("/boards", headers=_auth_header(token))
        assert r3.status_code == 200
        assert r3.json() == []

    def test_cascades_columns(self, client):
        token = _register(client, "user11")
        r = client.post("/boards", json={"title": "Cascade"}, headers=_auth_header(token))
        board_id = r.json()["id"]
        client.delete(f"/boards/{board_id}", headers=_auth_header(token))

        db = SessionLocal()
        cols = db.query(Column).filter(Column.board_id == board_id).all()
        assert len(cols) == 0
        db.close()

    def test_not_found(self, client):
        token = _register(client, "user12")
        r = client.delete("/boards/9999", headers=_auth_header(token))
        assert r.status_code == 404

    def test_wrong_owner_returns_404(self, client):
        t1 = _register(client, "owner_c")
        t2 = _register(client, "owner_d")
        r = client.post("/boards", json={"title": "Board"}, headers=_auth_header(t1))
        board_id = r.json()["id"]
        r2 = client.delete(f"/boards/{board_id}", headers=_auth_header(t2))
        assert r2.status_code == 404

        r3 = client.get("/boards", headers=_auth_header(t1))
        assert r3.status_code == 200
        assert len(r3.json()) == 1


class TestBoardAuth:
    def test_unauthenticated(self, client):
        assert client.get("/boards").status_code == 401
        assert client.post("/boards", json={"title": "X"}).status_code == 401
        assert client.put("/boards/1", json={"title": "X"}).status_code == 401
        assert client.delete("/boards/1").status_code == 401
