from fastapi.testclient import TestClient

from app.main import app


def calculate_xp(rewards: list[int]) -> int:
    return sum(rewards)


def test_calculate_xp():
    assert calculate_xp([20, 30, 25]) == 75


def test_empty_xp():
    assert calculate_xp([]) == 0


def test_health():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
