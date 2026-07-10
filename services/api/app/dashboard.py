from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DashboardAgendaItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    title: str
    starts_at: datetime
    ends_at: datetime
    conflict: bool = False


class DashboardSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    date: str
    agenda: list[DashboardAgendaItem]
    pending_approvals: int
    open_github_items: int
    risks: list[str]


def empty_dashboard(date: str) -> DashboardSummary:
    return DashboardSummary(date=date, agenda=[], pending_approvals=0, open_github_items=0, risks=[])

