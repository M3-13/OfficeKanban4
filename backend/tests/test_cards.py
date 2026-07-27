def test_create_card(client, auth_headers, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "A task"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "A task"
    assert data["description"] == ""
    assert data["position"] == 0
    assert data["column_id"] == test_column["id"]


def test_create_card_with_description(client, auth_headers, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Task", "description": "Details here"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert r.json()["description"] == "Details here"


def test_create_card_auto_position(client, auth_headers, test_column):
    client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "First"},
        headers=auth_headers,
    )
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Second"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert r.json()["position"] == 1


def test_list_cards_sorted(client, auth_headers, test_column):
    client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Z"},
        headers=auth_headers,
    )
    client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "A"},
        headers=auth_headers,
    )
    r = client.get(f"/columns/{test_column['id']}/cards", headers=auth_headers)
    assert r.status_code == 200
    cards = r.json()
    assert len(cards) == 2
    assert cards[0]["position"] < cards[1]["position"]


def test_update_card_title(client, auth_headers, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Old"},
        headers=auth_headers,
    )
    card_id = r.json()["id"]
    r2 = client.put(
        f"/cards/{card_id}",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert r2.status_code == 200
    assert r2.json()["title"] == "New Title"


def test_update_card_description(client, auth_headers, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Task"},
        headers=auth_headers,
    )
    card_id = r.json()["id"]
    r2 = client.put(
        f"/cards/{card_id}",
        json={"description": "Updated desc"},
        headers=auth_headers,
    )
    assert r2.status_code == 200
    assert r2.json()["description"] == "Updated desc"


def test_delete_card(client, auth_headers, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Delete Me"},
        headers=auth_headers,
    )
    card_id = r.json()["id"]
    r2 = client.delete(f"/cards/{card_id}", headers=auth_headers)
    assert r2.status_code == 204
    r3 = client.get(f"/columns/{test_column['id']}/cards", headers=auth_headers)
    assert r3.json() == []


def test_move_card_within_column(client, auth_headers, test_column):
    url = f"/columns/{test_column['id']}/cards"
    client.post(url, json={"title": "A"}, headers=auth_headers)
    client.post(url, json={"title": "B"}, headers=auth_headers)
    c3 = client.post(url, json={"title": "C"}, headers=auth_headers).json()

    r = client.put(
        f"/cards/{c3['id']}/move",
        json={"column_id": test_column["id"], "position": 0},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["position"] == 0

    cards = client.get(url, headers=auth_headers).json()
    titles = [c["title"] for c in cards]
    assert titles == ["C", "A", "B"]


def test_move_card_between_columns(client, auth_headers, test_board):
    col1 = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "Col A"},
        headers=auth_headers,
    ).json()
    col2 = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "Col B"},
        headers=auth_headers,
    ).json()

    client.post(
        f"/columns/{col1['id']}/cards",
        json={"title": "A1"},
        headers=auth_headers,
    )
    card = client.post(
        f"/columns/{col1['id']}/cards",
        json={"title": "A2"},
        headers=auth_headers,
    ).json()

    r = client.put(
        f"/cards/{card['id']}/move",
        json={"column_id": col2["id"], "position": 0},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["column_id"] == col2["id"]
    assert r.json()["position"] == 0

    col1_cards = client.get(f"/columns/{col1['id']}/cards", headers=auth_headers).json()
    assert len(col1_cards) == 1
    assert col1_cards[0]["position"] == 0

    col2_cards = client.get(f"/columns/{col2['id']}/cards", headers=auth_headers).json()
    assert len(col2_cards) == 1
    assert col2_cards[0]["title"] == "A2"


def test_move_card_to_end_of_column(client, auth_headers, test_column):
    url = f"/columns/{test_column['id']}/cards"
    c1 = client.post(url, json={"title": "A"}, headers=auth_headers).json()
    client.post(url, json={"title": "B"}, headers=auth_headers).json()

    r = client.put(
        f"/cards/{c1['id']}/move",
        json={"column_id": test_column["id"], "position": 5},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["position"] == 1

    cards = client.get(url, headers=auth_headers).json()
    assert cards[0]["title"] == "B"
    assert cards[1]["title"] == "A"


def test_card_ownership_chain_forbidden(client, auth_headers, auth_headers_other, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Secret"},
        headers=auth_headers,
    )
    card_id = r.json()["id"]

    r2 = client.put(f"/cards/{card_id}", json={"title": "Hijack"}, headers=auth_headers_other)
    assert r2.status_code == 403

    r3 = client.delete(f"/cards/{card_id}", headers=auth_headers_other)
    assert r3.status_code == 403


def test_card_list_ownership_forbidden(client, auth_headers_other, test_column):
    r = client.get(f"/columns/{test_column['id']}/cards", headers=auth_headers_other)
    assert r.status_code == 403


def test_create_card_ownership_forbidden(client, auth_headers_other, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Nope"},
        headers=auth_headers_other,
    )
    assert r.status_code == 403


def test_move_card_ownership_forbidden(client, auth_headers, auth_headers_other, test_column):
    card = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Steal me"},
        headers=auth_headers,
    ).json()
    r = client.put(
        f"/cards/{card['id']}/move",
        json={"column_id": test_column["id"], "position": 0},
        headers=auth_headers_other,
    )
    assert r.status_code == 403


def test_card_on_nonexistent_column(client, auth_headers):
    r = client.get("/columns/9999/cards", headers=auth_headers)
    assert r.status_code == 404


def test_card_title_validation(client, auth_headers, test_column):
    r = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": ""},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_move_card_nonexistent(client, auth_headers):
    r = client.put(
        "/cards/9999/move",
        json={"column_id": 1, "position": 0},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_move_card_to_nonexistent_column(client, auth_headers, test_column):
    card = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Task"},
        headers=auth_headers,
    ).json()
    r = client.put(
        f"/cards/{card['id']}/move",
        json={"column_id": 9999, "position": 0},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_move_card_reorders_source_column(client, auth_headers, test_board):
    col1 = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "Col A"},
        headers=auth_headers,
    ).json()
    col2 = client.post(
        f"/boards/{test_board['id']}/columns",
        json={"title": "Col B"},
        headers=auth_headers,
    ).json()

    client.post(
        f"/columns/{col1['id']}/cards",
        json={"title": "A1"},
        headers=auth_headers,
    )
    card = client.post(
        f"/columns/{col1['id']}/cards",
        json={"title": "A2"},
        headers=auth_headers,
    ).json()
    client.post(
        f"/columns/{col1['id']}/cards",
        json={"title": "A3"},
        headers=auth_headers,
    )

    client.put(
        f"/cards/{card['id']}/move",
        json={"column_id": col2["id"], "position": 0},
        headers=auth_headers,
    )

    col1_cards = client.get(f"/columns/{col1['id']}/cards", headers=auth_headers).json()
    assert len(col1_cards) == 2
    assert col1_cards[0]["position"] == 0
    assert col1_cards[1]["position"] == 1


def test_update_card_with_no_changes(client, auth_headers, test_column):
    card = client.post(
        f"/columns/{test_column['id']}/cards",
        json={"title": "Original", "description": "Desc"},
        headers=auth_headers,
    ).json()
    r = client.put(f"/cards/{card['id']}", json={}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["title"] == "Original"
    assert r.json()["description"] == "Desc"
