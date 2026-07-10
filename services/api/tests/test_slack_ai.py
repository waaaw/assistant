from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.ai_contracts import MorningBriefing, build_responses_request
from app.slack import acknowledge_command, approval_button_payload, parse_approval_command


def test_slack_ack_is_immediate_and_button_has_only_id() -> None:
    approval_id = uuid4()
    assert acknowledge_command().response_type == "ephemeral"
    assert approval_button_payload(approval_id) == {"approval_request_id": str(approval_id)}


def test_natural_language_approval_requires_exact_id() -> None:
    assert parse_approval_command(f"approve {uuid4()}")[0] == "approve"
    assert parse_approval_command("approve tomorrow") is None


def test_responses_request_requires_strict_structured_output() -> None:
    request = build_responses_request("prepare briefing")
    assert request["text"]["format"]["strict"] is True
    with pytest.raises(ValidationError):
        MorningBriefing.model_validate({"summary": "bad", "items": [{"title": "x"}], "risks": []})
