from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.approvals import Approval, ApprovalAlreadyDecided, CalendarWriteGateway, Decision
from app.calendar_sync import RemoteEvent
from app.planning import find_conflicts, find_free_windows


def event(start: int, end: int, title: str = "event") -> RemoteEvent:
    base = datetime(2026, 7, 11, tzinfo=timezone.utc)
    return RemoteEvent(title, title, base + timedelta(hours=start), base + timedelta(hours=end))


def test_conflicts_and_free_windows() -> None:
    events = [event(9, 11, "A"), event(10, 12, "B"), event(15, 16, "C")]
    assert len(find_conflicts(events)) == 1
    windows = find_free_windows(events, event(8, 8).starts_at, event(18, 18).starts_at)
    assert [(window.starts_at.hour, window.ends_at.hour) for window in windows] == [(8, 9), (12, 15), (16, 18)]


def test_approval_and_external_write_are_idempotent() -> None:
    approval = Approval(uuid4(), uuid4(), "calendar.create", "same-key", {"title": "Focus"})
    approval.decide(Decision.APPROVE)
    gateway = CalendarWriteGateway()
    assert gateway.execute_once(approval)["status"] == "executed"
    assert gateway.execute_once(approval)["status"] == "already_executed"
    with pytest.raises(ApprovalAlreadyDecided):
        approval.decide(Decision.REJECT)
