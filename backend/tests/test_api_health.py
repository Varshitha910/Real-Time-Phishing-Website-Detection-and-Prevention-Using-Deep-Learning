"""Tests for the FastAPI health endpoint."""

from fastapi.testclient import TestClient

from backend.app.main import app


def test_health_check() -> None:
    """The API should expose a simple health response."""

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
