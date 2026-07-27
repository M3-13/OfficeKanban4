def test_list_columns_default(client, auth_headers, test_board):
    r = client.get(f"/boards/{test_board['id']}/columns", headers=auth_headers)
    assert r.status_code == 200
    cols = r.json()
    assert len(cols) == 3
    titles = [c["title"] for c in cols]
    assert "To Do" in titles
    assert "In Progress" in titles
    assert "Done" in titles


def test_create_column(client, auth_headers, test_board):
    r = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "To Do"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "To Do"
    assert data["position"] == 3
    assert data["board_id"] == test_board["id"]


def test_create_column_auto_position(client, auth_headers, test_board):
    client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "First"},
        headers=auth_headers,
    )
    r = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "Second"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert r.json()["position"] == 4


def test_list_columns_sorted(client, auth_headers, test_board):
    client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "C"},
        headers=auth_headers,
    )
    client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "A"},
        headers=auth_headers,
    )
    client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "B"},
        headers=auth_headers,
    )
    r = client.get(f"/boards/{test_board['id']}/columns", headers=auth_headers)
    assert r.status_code == 200
    cols = r.json()
    assert len(cols) == 6
    assert cols[3]["title"] == "C"
    assert cols[4]["title"] == "A"
    assert cols[5]["title"] == "B"
    positions = [c["position"] for c in cols[3:]]
    assert positions == sorted(positions)


def test_update_column_title(client, auth_headers, test_column):
    r = client.put(
        f"/boards/{test_column['board_id']}/columns/{test_column['id']}",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["title"] == "New Title"


def test_delete_column(client, auth_headers, test_column):
    r = client.delete(
        f"/boards/{test_column['board_id']}/columns/{test_column['id']}",
        headers=auth_headers,
    )
    assert r.status_code == 204
    r2 = client.get(
        f"/boards/{test_column['board_id']}/columns",
        headers=auth_headers,
    )
    assert len(r2.json()) == 3


def test_delete_column_cascades_cards(client, auth_headers, test_column):
    client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Card"},
        headers=auth_headers,
    )
    r = client.delete(
        f"/boards/{test_column['board_id']}/columns/{test_column['id']}",
        headers=auth_headers,
    )
    assert r.status_code == 204

    r2 = client.delete(
        f"/boards/{test_column['board_id']}/columns/{test_column['id']}",
        headers=auth_headers,
    )
    assert r2.status_code == 404

    r3 = client.get(
        f"/boards/{test_column['board_id']}/columns",
        headers=auth_headers,
    )
    assert len(r3.json()) == 3


def test_column_on_nonexistent_board(client, auth_headers):
    r = client.get("/boards/9999/columns", headers=auth_headers)
    assert r.status_code == 404


def test_column_other_user_forbidden(client, auth_headers_other, test_board):
    r = client.get(f"/boards/{test_board['id']}/columns", headers=auth_headers_other)
    assert r.status_code == 403


def test_create_column_other_user_forbidden(client, auth_headers_other, test_board):
    r = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "Nope"},
        headers=auth_headers_other,
    )
    assert r.status_code == 403


def test_update_column_other_user_forbidden(client, auth_headers_other, test_column):
    r = client.put(
        f"/boards/{test_column['board_id']}/columns/{test_column['id']}",
        json={"title": "Hijack"},
        headers=auth_headers_other,
    )
    assert r.status_code == 403


def test_delete_column_other_user_forbidden(client, auth_headers_other, test_column):
    r = client.delete(
        f"/boards/{test_column['board_id']}/columns/{test_column['id']}",
        headers=auth_headers_other,
    )
    assert r.status_code == 403


def test_delete_nonexistent_column(client, auth_headers, test_board):
    r = client.delete(f"/boards/{test_board['id']}/columns/9999", headers=auth_headers)
    assert r.status_code == 404


def test_column_title_validation(client, auth_headers, test_board):
    r = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": ""},
        headers=auth_headers,
    )
    assert r.status_code == 422
