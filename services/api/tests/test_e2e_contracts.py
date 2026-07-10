from datetime import datetime, timezone
from uuid import uuid4

from app.approvals import Approval, CalendarWriteGateway, Decision
from app.calendar_sync import CalendarSyncCoordinator, CalendarSyncState


def test_approval_e2e_is_exactly_once() -> None:
    approval = Approval(uuid4(), uuid4(), "calendar.create", "e2e-key", {"title": "Focus"})
    approval.decide(Decision.APPROVE)
    gateway = CalendarWriteGateway()
    assert gateway.execute_once(approval)["status"] == "executed"
    assert gateway.execute_once(approval)["status"] == "already_executed"

