from datetime import datetime, timedelta, timezone

from app.calendar_sync import CalendarSyncCoordinator, CalendarSyncState, RemoteEvent, SyncPage, SyncTokenExpired


class FakeCalendar:
    def __init__(self) -> None:
        self.calls: list[tuple[str | None, bool]] = []
        self.renewals = 0

    def list_changes(self, sync_token: str | None, full_resync: bool = False) -> SyncPage:
        self.calls.append((sync_token, full_resync))
        if sync_token == "stale":
            raise SyncTokenExpired
        return SyncPage([], "next-token", datetime.now(timezone.utc) + timedelta(hours=1))

    def renew_channel(self) -> datetime:
        self.renewals += 1
        return datetime.now(timezone.utc) + timedelta(hours=1)


def test_410_equivalent_forces_full_resync() -> None:
    adapter = FakeCalendar()
    state = CalendarSyncState(sync_token="stale")
    page = CalendarSyncCoordinator(adapter).sync(state)
    assert adapter.calls == [("stale", False), (None, True)]
    assert state.sync_token == page.next_sync_token


def test_channel_renews_only_inside_window() -> None:
    adapter = FakeCalendar()
    coordinator = CalendarSyncCoordinator(adapter, renew_before=timedelta(minutes=15))
    now = datetime.now(timezone.utc)
    state = CalendarSyncState(channel_expires_at=now + timedelta(minutes=5))
    assert coordinator.renew_if_needed(state, now) is True
    assert adapter.renewals == 1
    state.channel_expires_at = now + timedelta(hours=1)
    assert coordinator.renew_if_needed(state, now) is False
