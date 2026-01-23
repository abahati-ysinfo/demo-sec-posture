"""add_is_protected_to_users

Revision ID: a7ce31896fc5
Revises: 1763376500
Create Date: 2025-11-18 10:01:01.462581

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a7ce31896fc5"
down_revision = "1763376500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_protected", sa.Boolean(), nullable=False, server_default="false"),
    )

    op.create_index(
        op.f("ix_users_is_protected"), "users", ["is_protected"], unique=False
    )

    op.execute(
        """
        UPDATE users 
        SET is_protected = true 
        WHERE email IN ('aadish.bahati@echostor.com', 'admin@echostor.com')
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_users_is_protected"), table_name="users")

    op.drop_column("users", "is_protected")
