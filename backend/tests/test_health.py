from fastapi.testclient import TestClient

from app.main import app


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "WareX API"
    assert response.json()["status"] == "running"


def test_liveness_endpoint():
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_database_readiness():
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"
