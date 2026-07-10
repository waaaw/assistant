import hashlib
import hmac

import pytest

from app.github_integration import DeliveryDeduper, DuplicateDelivery, FakeGitHubReader, GitHubIssue, verify_webhook_signature


def test_webhook_signature_is_constant_time_comparable() -> None:
    body = b'{"action":"opened"}'
    digest = hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert verify_webhook_signature("secret", body, f"sha256={digest}")
    assert not verify_webhook_signature("secret", body, "sha256=bad")


def test_delivery_is_processed_once() -> None:
    deduper = DeliveryDeduper()
    deduper.claim("delivery-1")
    with pytest.raises(DuplicateDelivery):
        deduper.claim("delivery-1")


def test_fake_reader_returns_only_open_issues() -> None:
    reader = FakeGitHubReader([GitHubIssue(1, "Open", "https://github/1", "open"), GitHubIssue(2, "Done", "https://github/2", "closed")])
    assert [issue.number for issue in reader.list_open_issues("waaaw", "assistant")] == [1]
