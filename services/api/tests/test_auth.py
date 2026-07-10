from fastapi.testclient import TestClient

from app.main import app


def test_google_start_uses_oidc_scopes() -> None:
    response = TestClient(app).get("/auth/google/start")
    assert response.status_code == 200
    assert "openid" in response.json()["authorization_url"]
    assert "oauth_state" in response.cookies


def test_google_callback_rejects_invalid_state() -> None:
    response = TestClient(app).get("/auth/google/callback?state=bad&code=abc")
    assert response.status_code == 400
