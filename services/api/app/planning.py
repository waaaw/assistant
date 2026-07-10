from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.calendar_sync import RemoteEvent


@dataclass(frozen=True)
class TimeWindow:
    starts_at: datetime
    ends_at: datetime


def find_conflicts(events: list[RemoteEvent]) -> list[tuple[RemoteEvent, RemoteEvent]]:
    ordered = sorted(events, key=lambda event: event.starts_at)
    return [(left, right) for left, right in zip(ordered, ordered[1:]) if left.ends_at > right.starts_at]


def find_free_windows(events: list[RemoteEvent], day_start: datetime, day_end: datetime, minimum: timedelta = timedelta(minutes=30)) -> list[TimeWindow]:
    busy = sorted((event for event in events if event.ends_at > day_start and event.starts_at < day_end), key=lambda event: event.starts_at)
    windows: list[TimeWindow] = []
    cursor = day_start
    for event in busy:
        start = max(cursor, day_start)
        end = min(event.starts_at, day_end)
        if end - start >= minimum:
            windows.append(TimeWindow(start, end))
        cursor = max(cursor, event.ends_at)
    if day_end - cursor >= minimum:
        windows.append(TimeWindow(cursor, day_end))
    return windows


def utc(value: datetime) -> datetime:
    return value.astimezone(timezone.utc)

