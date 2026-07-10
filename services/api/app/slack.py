from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SlackAck:
    text: str
    response_type: str = "ephemeral"


def acknowledge_command() -> SlackAck:
    return SlackAck("요청을 받았습니다. 처리 중입니다.")


def approval_button_payload(approval_request_id: UUID) -> dict:
    return {"approval_request_id": str(approval_request_id)}


def parse_approval_command(text: str) -> tuple[str, UUID] | None:
    parts = text.strip().split()
    if len(parts) != 2 or parts[0].lower() not in {"approve", "reject", "승인", "거절"}:
        return None
    try:
        action = "approve" if parts[0].lower() in {"approve", "승인"} else "reject"
        return action, UUID(parts[1])
    except ValueError:
        return None

