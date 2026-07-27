"""Tests for CRUD behavior, validation, pagination, and state isolation."""

from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


def create_item(client: TestClient, name: str) -> dict:
    response = client.post(
        "/api/v1/items",
        json={"name": name, "description": f"Notes for {name}"},
    )
    assert response.status_code == 201
    return response.json()


def test_item_create_list_get_and_delete(client: TestClient) -> None:
    created = create_item(client, "FastAPI book")

    assert created == {
        "id": 1,
        "name": "FastAPI book",
        "description": "Notes for FastAPI book",
    }
    assert client.get("/api/v1/items").json() == [created]
    assert client.get("/api/v1/items/1").json() == created

    delete_response = client.delete("/api/v1/items/1")
    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert client.get("/api/v1/items/1").status_code == 404


def test_list_items_uses_validated_pagination(client: TestClient) -> None:
    create_item(client, "one")
    second = create_item(client, "two")
    third = create_item(client, "three")

    response = client.get("/api/v1/items", params={"offset": 1, "limit": 1})

    assert response.status_code == 200
    assert response.json() == [second]
    assert third["id"] == 3


def test_item_can_be_updated(client: TestClient) -> None:
    create_item(client, "first name")

    response = client.patch(
        "/api/v1/items/1",
        json={"name": "updated name", "description": "Updated through PATCH"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "updated name",
        "description": "Updated through PATCH",
    }
    assert client.get("/api/v1/items/1").json() == response.json()


def test_updating_missing_item_returns_404(client: TestClient) -> None:
    response = client.patch("/api/v1/items/999", json={"name": "missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Item 999 was not found"}


def test_invalid_item_is_rejected(client: TestClient) -> None:
    response = client.post("/api/v1/items", json={"name": ""})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "name"]


def test_invalid_pagination_is_rejected(client: TestClient) -> None:
    negative_offset = client.get("/api/v1/items", params={"offset": -1})
    excessive_limit = client.get("/api/v1/items", params={"limit": 101})

    assert negative_offset.status_code == 422
    assert excessive_limit.status_code == 422


def test_missing_item_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item 999 was not found"}


def test_app_instances_do_not_share_item_state() -> None:
    settings = Settings(_env_file=None)

    with TestClient(create_app(settings)) as first_client:
        create_item(first_client, "temporary")
        assert len(first_client.get("/api/v1/items").json()) == 1

    with TestClient(create_app(settings)) as second_client:
        assert second_client.get("/api/v1/items").json() == []
