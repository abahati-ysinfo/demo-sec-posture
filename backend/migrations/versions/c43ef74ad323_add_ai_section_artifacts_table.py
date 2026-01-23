"""add_ai_section_artifacts_table

Revision ID: c43ef74ad323
Revises: 2da9d700c89f
Create Date: 2025-11-11 21:15:36.025795

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c43ef74ad323"
down_revision = "2da9d700c89f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    json_type = (
        postgresql.JSONB(astext_type=sa.Text())
        if bind.dialect.name == "postgresql"
        else sa.JSON()
    )

    op.create_table(
        "ai_section_artifacts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "report_id",
            sa.String(36),
            sa.ForeignKey("reports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("section_id", sa.String(100), nullable=False),
        sa.Column("artifact_json", json_type, nullable=False),
        sa.Column("storage_uri", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    op.create_index("idx_artifacts_report", "ai_section_artifacts", ["report_id"])

    op.create_index(
        "idx_artifacts_report_section",
        "ai_section_artifacts",
        ["report_id", "section_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("idx_artifacts_report_section", table_name="ai_section_artifacts")
    op.drop_index("idx_artifacts_report", table_name="ai_section_artifacts")
    op.drop_table("ai_section_artifacts")
