from worker_app.briefing import build_briefing_input, validate_briefing


def test_worker_briefing_contract_is_standalone() -> None:
    payload = {"summary": "all good", "items": [], "risks": []}
    assert validate_briefing(payload).summary == "all good"
    assert "Untrusted calendar data" in build_briefing_input([])
