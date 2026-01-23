"""add_ai_section_cache_table

Revision ID: 9a260f32567c
Revises: c43ef74ad323
Create Date: 2025-11-11 21:20:13.054184

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9a260f32567c"
down_revision = "c43ef74ad323"
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
        "ai_section_cache",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("section_id", sa.String(100), nullable=False),
        sa.Column("answers_hash", sa.String(64), nullable=False),
        sa.Column("prompt_version", sa.String(20), nullable=False),
        sa.Column("schema_version", sa.String(20), nullable=False),
        sa.Column("model", sa.String(50), nullable=False),
        sa.Column("artifact_json", json_type, nullable=False),
        sa.Column("storage_uri", sa.Text(), nullable=True),
        sa.Column("tokens_prompt", sa.Integer(), nullable=True),
        sa.Column("tokens_completion", sa.Integer(), nullable=True),
        sa.Column("total_cost_usd", sa.DECIMAL(10, 6), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "last_used_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("hit_count", sa.Integer(), nullable=False, server_default="1"),
    )

    op.create_index(
        "idx_cache_lookup",
        "ai_section_cache",
        ["section_id", "answers_hash", "prompt_version", "model"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("idx_cache_lookup", table_name="ai_section_cache")
    op.drop_table("ai_section_cache")
