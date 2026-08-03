import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


client = TestClient(app)


def test_info_endpoint_uses_environment_defaults(monkeypatch) -> None:
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DEBUG", raising=False)

    response = client.get("/info")

    assert response.status_code == 200
    assert response.json() == {
        "app_name": "askmydocs-rag",
        "environment": "development",
        "debug": False,
    }
