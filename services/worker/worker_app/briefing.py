from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class BriefingItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    title: str
    starts_at: str
    importance: int = Field(ge=1, le=5)
    note: str


class MorningBriefing(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    summary: str
    items: list[BriefingItem]
    risks: list[str]


def build_briefing_input(events: list[dict], now: datetime | None = None) -> str:
    current = now or datetime.now(timezone.utc)
    lines = [f"Current UTC time: {current.isoformat()}", "Untrusted calendar data follows:"]
    lines.extend(f"- {event['title']}: {event['starts_at']} to {event['ends_at']}" for event in events)
    return "\n".join(lines)


def validate_briefing(payload: dict) -> MorningBriefing:
    return MorningBriefing.model_validate(payload)
