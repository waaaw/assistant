import hashlib
import hmac
from dataclasses import dataclass
from typing import Protocol


def verify_webhook_signature(secret: str, body: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


class DuplicateDelivery(Exception):
    pass


class DeliveryDeduper:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def claim(self, delivery_id: str) -> None:
        if delivery_id in self._seen:
            raise DuplicateDelivery(delivery_id)
        self._seen.add(delivery_id)


@dataclass(frozen=True)
class GitHubIssue:
    number: int
    title: str
    url: str
    state: str


class GitHubReader(Protocol):
    def list_open_issues(self, owner: str, repo: str) -> list[GitHubIssue]: ...


class FakeGitHubReader:
    def __init__(self, issues: list[GitHubIssue] | None = None) -> None:
        self.issues = issues or []

    def list_open_issues(self, owner: str, repo: str) -> list[GitHubIssue]:
        return [issue for issue in self.issues if issue.state == "open"]

