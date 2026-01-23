"""add_is_admin_column_to_users

Revision ID: 9cbe6669eb84
Revises: d1e2f3a4b5c6
Create Date: 2025-09-18 13:57:13.682721

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9cbe6669eb84"
down_revision = "d1e2f3a4b5c6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("is_admin", sa.Boolean(), nullable=True, default=False)
    )

    op.execute("UPDATE users SET is_admin = FALSE WHERE is_admin IS NULL")

    op.alter_column("users", "is_admin", nullable=False)


def downgrade() -> None:
    op.drop_column("users", "is_admin")
