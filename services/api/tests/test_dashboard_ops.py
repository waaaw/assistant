from fastapi.testclient import TestClient

from app.main import app
from app.ops import deletion_plan, redact_secrets


def test_dashboard_and_request_id() -> None:
    response = TestClient(app).get("/dashboard/summary", headers={"x-request-id": "test-request"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "test-request"
    assert response.json()["pending_approvals"] == 0


def test_readiness_and_secret_redaction() -> None:
    assert TestClient(app).get("/ready").json()["status"] == "ready"
    assert "secret" not in redact_secrets("Bearer secret")
    assert deletion_plan("user-1")["action"] == "delete_user_cascade"
