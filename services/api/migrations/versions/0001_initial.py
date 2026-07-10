"""Initial assistant domain schema."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    uuid = postgresql.UUID(as_uuid=True)
    jsonb = postgresql.JSONB()
    op.create_table("users", sa.Column("id", uuid, primary_key=True), sa.Column("email", sa.String(320), nullable=False, unique=True), sa.Column("display_name", sa.String(200)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("external_accounts", sa.Column("id", uuid, primary_key=True), sa.Column("user_id", uuid, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("provider", sa.String(40), nullable=False), sa.Column("provider_subject", sa.String(255), nullable=False), sa.Column("encrypted_access_token", sa.Text()), sa.Column("encrypted_refresh_token", sa.Text()), sa.Column("expires_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.UniqueConstraint("user_id", "provider", "provider_subject", name="uq_external_account_subject"))
    op.create_table("calendar_events", sa.Column("id", uuid, primary_key=True), sa.Column("user_id", uuid, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("provider", sa.String(40), nullable=False), sa.Column("provider_event_id", sa.String(255), nullable=False), sa.Column("title", sa.String(500), nullable=False), sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False), sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False), sa.Column("raw_payload", jsonb, nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.UniqueConstraint("user_id", "provider", "provider_event_id", name="uq_calendar_event_provider"))
    op.create_index("ix_calendar_events_user_start", "calendar_events", ["user_id", "starts_at"])
    op.create_table("approval_requests", sa.Column("id", uuid, primary_key=True), sa.Column("user_id", uuid, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("action_type", sa.String(80), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("payload", jsonb, nullable=False), sa.Column("idempotency_key", sa.String(255), nullable=False, unique=True), sa.Column("decided_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_approval_requests_user_status", "approval_requests", ["user_id", "status"])
    op.create_table("automation_grants", sa.Column("id", uuid, primary_key=True), sa.Column("user_id", uuid, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True), sa.Column("grant_type", sa.String(80), nullable=False), sa.Column("enabled_at", sa.DateTime(timezone=True)), sa.Column("revoked_at", sa.DateTime(timezone=True)))
    op.create_table("webhook_deliveries", sa.Column("id", uuid, primary_key=True), sa.Column("provider", sa.String(40), nullable=False), sa.Column("delivery_id", sa.String(255), nullable=False, unique=True), sa.Column("received_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))


def downgrade() -> None:
    op.drop_table("webhook_deliveries")
    op.drop_table("automation_grants")
    op.drop_index("ix_approval_requests_user_status", table_name="approval_requests")
    op.drop_table("approval_requests")
    op.drop_index("ix_calendar_events_user_start", table_name="calendar_events")
    op.drop_table("calendar_events")
    op.drop_table("external_accounts")
    op.drop_table("users")

