from typing import Any

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


def responses_json_schema() -> dict[str, Any]:
    return {
        "type": "json_schema",
        "name": "morning_briefing",
        "strict": True,
        "schema": MorningBriefing.model_json_schema(),
    }


def build_responses_request(input_text: str, model: str = "gpt-5-mini") -> dict[str, Any]:
    return {
        "model": model,
        "input": input_text,
        "text": {"format": responses_json_schema()},
    }

