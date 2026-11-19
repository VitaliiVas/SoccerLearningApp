from app.auth import get_current_user
from app.main import app
from tests.conftest import TEST_CLERK_ID


def test_authenticated_user(client):
    response = client.get("/me")

    assert response.status_code == 200
    assert response.json()["clerk_id"] == TEST_CLERK_ID


def test_complete_lesson_without_auth(client):
    # Drop the auth override so the real get_current_user runs.
    original_override = app.dependency_overrides.pop(get_current_user, None)

    try:
        # No Authorization header, and no lesson needed: the auth
        # dependency rejects the request before the endpoint runs.
        response = client.post("/lessons/1/complete")

        assert response.status_code == 401
    finally:
        if original_override is not None:
            app.dependency_overrides[get_current_user] = original_override
