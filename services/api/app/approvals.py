from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class Decision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"


class ApprovalAlreadyDecided(Exception):
    pass


@dataclass
class Approval:
    id: UUID
    user_id: UUID
    action_type: str
    idempotency_key: str
    payload: dict
    status: str = "pending"

    def decide(self, decision: Decision) -> None:
        if self.status != "pending":
            raise ApprovalAlreadyDecided(self.idempotency_key)
        self.status = "approved" if decision == Decision.APPROVE else "rejected"


class CalendarWriteGateway:
    def __init__(self) -> None:
        self.executed_keys: set[str] = set()

    def execute_once(self, approval: Approval) -> dict:
        if approval.status != "approved":
            raise ValueError("approval is not approved")
        if approval.idempotency_key in self.executed_keys:
            return {"status": "already_executed", "idempotency_key": approval.idempotency_key}
        self.executed_keys.add(approval.idempotency_key)
        return {"status": "executed", "idempotency_key": approval.idempotency_key}

