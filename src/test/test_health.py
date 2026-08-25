from fastapi.testclient import TestClient
from httpx import Response

from src.main import app

client = TestClient(app)


def test_health():
    response: Response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
