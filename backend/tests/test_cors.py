import pytest

from app.auth import AUTHORIZED_PARTIES

ORIGIN = sorted(AUTHORIZED_PARTIES)[0]


@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_cors_preflight_allows_api_methods(client, method):
    response = client.options(
        "/lessons/1",
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "Authorization",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ORIGIN
