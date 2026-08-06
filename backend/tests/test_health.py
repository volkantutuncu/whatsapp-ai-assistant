"""Health endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_check() -> None:
    """Verify that the health endpoint responds successfully."""

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
