"""add attempt_number to assessments table

Revision ID: f1a2b3c4d5e6
Revises: ea99a564b1f9
Create Date: 2025-11-12 09:14:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f1a2b3c4d5e6"
down_revision = "ea99a564b1f9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "assessments", sa.Column("attempt_number", sa.Integer(), nullable=True)
    )

    op.execute("UPDATE assessments SET attempt_number = 1 WHERE attempt_number IS NULL")

    op.alter_column(
        "assessments",
        "attempt_number",
        nullable=False,
        server_default=sa.text("1"),
    )


def downgrade() -> None:
    op.drop_column("assessments", "attempt_number")
