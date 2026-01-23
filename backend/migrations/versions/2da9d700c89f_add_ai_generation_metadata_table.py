"""add_ai_generation_metadata_table

Revision ID: 2da9d700c89f
Revises: 1762153457
Create Date: 2025-11-11 21:11:22.860893

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2da9d700c89f"
down_revision = "1762153457"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_generation_metadata",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "report_id",
            sa.String(36),
            sa.ForeignKey("reports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("section_id", sa.String(100), nullable=True),
        sa.Column("prompt_version", sa.String(20), nullable=False),
        sa.Column("schema_version", sa.String(20), nullable=False),
        sa.Column("model", sa.String(50), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("max_tokens", sa.Integer(), nullable=False),
        sa.Column("tokens_prompt", sa.Integer(), nullable=True),
        sa.Column("tokens_completion", sa.Integer(), nullable=True),
        sa.Column("total_cost_usd", sa.DECIMAL(10, 6), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    op.create_index(
        "idx_ai_metadata_report_section",
        "ai_generation_metadata",
        ["report_id", "section_id"],
    )


def downgrade() -> None:
    op.drop_index("idx_ai_metadata_report_section", table_name="ai_generation_metadata")
    op.drop_table("ai_generation_metadata")
