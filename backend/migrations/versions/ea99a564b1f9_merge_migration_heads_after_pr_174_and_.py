"""merge migration heads after PR 174 and 175

Revision ID: ea99a564b1f9
Revises: 9a260f32567c, e1f2g3h4i5j6
Create Date: 2025-11-12 06:16:53.445187

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ea99a564b1f9"
down_revision = ("9a260f32567c", "e1f2g3h4i5j6")
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "ai_generation_metadata" in inspector.get_table_names():
        existing_columns = {
            col["name"] for col in inspector.get_columns("ai_generation_metadata")
        }

        if "attempt_count" not in existing_columns:
            op.add_column(
                "ai_generation_metadata",
                sa.Column(
                    "attempt_count", sa.Integer(), nullable=False, server_default="1"
                ),
            )
        if "error_code" not in existing_columns:
            op.add_column(
                "ai_generation_metadata",
                sa.Column("error_code", sa.String(length=50), nullable=True),
            )
        if "error_message" not in existing_columns:
            op.add_column(
                "ai_generation_metadata",
                sa.Column("error_message", sa.String(), nullable=True),
            )
        if "fallback_model" not in existing_columns:
            op.add_column(
                "ai_generation_metadata",
                sa.Column("fallback_model", sa.String(length=50), nullable=True),
            )
        if "is_degraded" not in existing_columns:
            op.add_column(
                "ai_generation_metadata",
                sa.Column(
                    "is_degraded", sa.Integer(), nullable=False, server_default="0"
                ),
            )
        if "last_retry_at" not in existing_columns:
            op.add_column(
                "ai_generation_metadata",
                sa.Column("last_retry_at", sa.DateTime(timezone=True), nullable=True),
            )


def downgrade() -> None:
    pass
