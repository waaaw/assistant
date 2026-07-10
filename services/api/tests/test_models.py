from app.models import ApprovalRequest, AutomationGrant, CalendarEvent, ExternalAccount, WebhookDelivery


def test_domain_tables_have_user_boundary() -> None:
    assert "user_id" in ApprovalRequest.__table__.c
    assert "user_id" in CalendarEvent.__table__.c
    assert "user_id" in ExternalAccount.__table__.c
    assert "user_id" in AutomationGrant.__table__.c


def test_webhook_delivery_has_unique_delivery_id() -> None:
    assert WebhookDelivery.__table__.c.delivery_id.unique is True

