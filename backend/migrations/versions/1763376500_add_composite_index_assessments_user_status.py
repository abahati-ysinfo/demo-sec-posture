"""add composite index on assessments user_id and status

Revision ID: 1763376500
Revises: 575105e0b6ed
Create Date: 2025-11-17 10:55:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "1763376500"
down_revision = "575105e0b6ed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add composite index for queries filtering by both user_id and status
    # This optimizes queries like: SELECT * FROM assessments WHERE user_id = ? AND status = ?
    op.create_index(
        "ix_assessments_user_id_status",
        "assessments",
        ["user_id", "status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_assessments_user_id_status", table_name="assessments")
