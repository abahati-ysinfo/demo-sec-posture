"""add assessment_intake_sessions table

Revision ID: 1763463955
Revises: f1a2b3c4d5e6
Create Date: 2025-11-18 11:05:55.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1763463955"
down_revision = "a7ce31896fc5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect_name = bind.dialect.name
    json_type = postgresql.JSONB() if dialect_name == "postgresql" else sa.JSON()

    op.create_table(
        "assessment_intake_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_profile_json", json_type, nullable=False),
        sa.Column("ai_raw_response_json", json_type, nullable=True),
        sa.Column("final_selected_section_ids", json_type, nullable=True),
        sa.Column("time_preference", sa.String(20), nullable=True),
        sa.Column("used_fallback", sa.Boolean(), default=False, nullable=False),
    )

    op.create_index(
        "ix_assessment_intake_sessions_user_id",
        "assessment_intake_sessions",
        ["user_id"],
    )

    op.create_index(
        "ix_assessment_intake_sessions_created_at",
        "assessment_intake_sessions",
        ["created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_assessment_intake_sessions_created_at",
        table_name="assessment_intake_sessions",
    )
    op.drop_index(
        "ix_assessment_intake_sessions_user_id", table_name="assessment_intake_sessions"
    )
    op.drop_table("assessment_intake_sessions")
