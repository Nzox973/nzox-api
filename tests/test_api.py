def test_registration_validates_password_and_never_returns_hash(client):
    weak = client.post(
        "/auth/register",
        json={"email": "weak@example.com", "username": "weak", "password": "short"},
    )
    assert weak.status_code == 422

    created = client.post(
        "/auth/register",
        json={
            "email": "enzo@example.com",
            "username": "enzo",
            "password": "Strong-password-123!",
        },
    )
    assert created.status_code == 201
    assert created.json()["email"] == "enzo@example.com"
    assert "password" not in created.json()
    assert "hashed_password" not in created.json()


def test_public_user_responses_never_expose_email(client, auth_headers):
    owner, headers = auth_headers("owner")

    public_item = client.post(
        "/items/",
        headers=headers,
        json={"title": "Public", "is_public": True},
    )
    assert public_item.status_code == 201
    private_item = client.post(
        "/items/",
        headers=headers,
        json={"title": "Private", "is_public": False},
    )
    assert private_item.status_code == 201

    listing = client.get("/users/", headers=headers)
    assert listing.status_code == 200
    assert all("email" not in user for user in listing.json())

    profile = client.get(f"/users/{owner['id']}")
    assert profile.status_code == 200
    assert "email" not in profile.json()
    assert [item["title"] for item in profile.json()["items"]] == ["Public"]


def test_private_item_is_visible_only_to_its_owner(client, auth_headers):
    _, owner_headers = auth_headers("owner")
    _, other_headers = auth_headers("other")

    created = client.post(
        "/items/",
        headers=owner_headers,
        json={"title": "Secret", "description": "Private", "is_public": False},
    )
    assert created.status_code == 201
    item_id = created.json()["id"]

    assert client.get(f"/items/{item_id}").status_code == 404
    assert client.patch(
        f"/items/{item_id}",
        headers=other_headers,
        json={"title": "Stolen"},
    ).status_code == 404
    assert client.delete(f"/items/{item_id}", headers=other_headers).status_code == 404

    mine = client.get("/items/me", headers=owner_headers)
    assert mine.status_code == 200
    assert mine.json()[0]["title"] == "Secret"


def test_public_item_can_be_read_without_authentication(client, auth_headers):
    _, headers = auth_headers("publisher")
    created = client.post(
        "/items/",
        headers=headers,
        json={"title": "Visible", "is_public": True},
    )
    response = client.get(f"/items/{created.json()['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Visible"


def test_item_patch_rejects_null_for_required_fields(client, auth_headers):
    _, headers = auth_headers("publisher")
    created = client.post(
        "/items/",
        headers=headers,
        json={"title": "Stable", "is_public": True},
    )
    item_id = created.json()["id"]

    for payload in ({"title": None}, {"is_public": None}):
        response = client.patch(f"/items/{item_id}", headers=headers, json=payload)
        assert response.status_code == 422

    unchanged = client.get(f"/items/{item_id}")
    assert unchanged.status_code == 200
    assert unchanged.json()["title"] == "Stable"
    assert unchanged.json()["is_public"] is True


def test_cors_allows_only_configured_origin(client):
    allowed = client.options(
        "/items/",
        headers={
            "Origin": "http://testserver",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert allowed.status_code == 200
    assert allowed.headers["access-control-allow-origin"] == "http://testserver"

    denied = client.options(
        "/items/",
        headers={
            "Origin": "https://example.invalid",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" not in denied.headers


def test_user_can_delete_only_own_account(client, auth_headers):
    owner, _owner_headers = auth_headers("owner")
    other, other_headers = auth_headers("other")

    forbidden = client.delete(f"/users/{owner['id']}", headers=other_headers)
    assert forbidden.status_code == 403

    deleted = client.delete(f"/users/{other['id']}", headers=other_headers)
    assert deleted.status_code == 204
