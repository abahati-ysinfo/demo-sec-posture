"""Convert assessment_responses.answer_value to JSONB

Revision ID: 6a3e3285b47f
Revises: 3f8a9b2c1d5e
Create Date: 2025-09-18 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6a3e3285b47f"
down_revision = "3f8a9b2c1d5e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE assessment_responses "
        "ALTER COLUMN answer_value TYPE JSONB USING answer_value::jsonb"
    )
    op.alter_column(
        "assessment_responses",
        "answer_value",
        existing_type=sa.Text(),
        nullable=True,
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE assessment_responses "
        "ALTER COLUMN answer_value TYPE TEXT USING answer_value::text"
    )
    op.alter_column(
        "assessment_responses",
        "answer_value",
        existing_type=sa.Text(),
        nullable=True,
    )
