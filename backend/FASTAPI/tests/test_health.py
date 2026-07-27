"""Health, documentation, settings, and middleware tests."""

import logging

from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


def test_health_returns_status_and_environment(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "local"}


def test_environment_settings_can_be_overridden(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "Practice Backend")
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    settings = Settings(_env_file=None)

    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/health")
        openapi = client.get("/openapi.json").json()

    assert response.json()["environment"] == "testing"
    assert openapi["info"]["title"] == "Practice Backend"
    assert settings.log_level == "DEBUG"


def test_api_documentation_is_available(client: TestClient) -> None:
    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200

    openapi_response = client.get("/openapi.json")
    assert openapi_response.status_code == 200
    assert "/api/v1/health" in openapi_response.json()["paths"]
    assert "/api/v1/items" in openapi_response.json()["paths"]


def test_request_id_is_generated_and_custom_value_is_propagated(
    client: TestClient,
) -> None:
    generated = client.get("/api/v1/health")
    supplied = client.get(
        "/api/v1/health",
        headers={"X-Request-ID": "learning-request-123"},
    )

    assert generated.headers["X-Request-ID"]
    assert float(generated.headers["X-Process-Time-Ms"]) >= 0
    assert supplied.headers["X-Request-ID"] == "learning-request-123"


def test_lifespan_writes_startup_and_shutdown_logs(caplog) -> None:
    settings = Settings(log_level="INFO", _env_file=None)

    with caplog.at_level(logging.INFO, logger="app.main"):
        with TestClient(create_app(settings)):
            pass

    assert "application_started" in caplog.text
    assert "application_stopped" in caplog.text
