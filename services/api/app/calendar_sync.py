from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol


class SyncTokenExpired(Exception):
    pass


@dataclass(frozen=True)
class RemoteEvent:
    provider_event_id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    status: str = "confirmed"


@dataclass(frozen=True)
class SyncPage:
    events: list[RemoteEvent]
    next_sync_token: str | None
    channel_expires_at: datetime | None


class CalendarAdapter(Protocol):
    def list_changes(self, sync_token: str | None, full_resync: bool = False) -> SyncPage: ...

    def renew_channel(self) -> datetime: ...


@dataclass
class CalendarSyncState:
    sync_token: str | None = None
    channel_expires_at: datetime | None = None


class CalendarSyncCoordinator:
    def __init__(self, adapter: CalendarAdapter, renew_before: timedelta = timedelta(minutes=15)) -> None:
        self.adapter = adapter
        self.renew_before = renew_before

    def sync(self, state: CalendarSyncState) -> SyncPage:
        try:
            page = self.adapter.list_changes(state.sync_token)
        except SyncTokenExpired:
            page = self.adapter.list_changes(None, full_resync=True)
        state.sync_token = page.next_sync_token
        state.channel_expires_at = page.channel_expires_at
        return page

    def renew_if_needed(self, state: CalendarSyncState, now: datetime | None = None) -> bool:
        current = now or datetime.now(timezone.utc)
        if state.channel_expires_at is None or state.channel_expires_at - current <= self.renew_before:
            state.channel_expires_at = self.adapter.renew_channel()
            return True
        return False

