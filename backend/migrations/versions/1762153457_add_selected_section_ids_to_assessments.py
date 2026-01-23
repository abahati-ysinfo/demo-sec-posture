"""add selected_section_ids to assessments

Revision ID: 1762153457
Revises: d5f251975256
Create Date: 2025-11-03 07:05:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1762153457"
down_revision = "d5f251975256"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "assessments",
        sa.Column("selected_section_ids", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("assessments", "selected_section_ids")
