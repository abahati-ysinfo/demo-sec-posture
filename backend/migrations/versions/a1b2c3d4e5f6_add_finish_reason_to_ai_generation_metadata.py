"""add finish_reason to ai_generation_metadata table

Revision ID: a1b2c3d4e5f6
Revises: f1a2b3c4d5e6
Create Date: 2025-11-12 10:48:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "ai_generation_metadata",
        sa.Column("finish_reason", sa.String(length=50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("ai_generation_metadata", "finish_reason")
