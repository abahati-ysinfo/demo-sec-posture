"""Add created_at and updated_at timestamps to assessments table

Revision ID: 3f8a9b2c1d5e
Revises: 2d4eb9575cd4
Create Date: 2025-09-17 04:59:17.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3f8a9b2c1d5e"
down_revision = "2d4eb9575cd4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "assessments",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
    )
    op.add_column(
        "assessments",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("assessments", "updated_at")
    op.drop_column("assessments", "created_at")
