"""add comment and consultation fields to assessments

Revision ID: d1e2f3a4b5c6
Revises: 0c55c907445b
Create Date: 2025-09-18 12:19:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d1e2f3a4b5c6"
down_revision = "0c55c907445b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "assessments", sa.Column("consultation_interest", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "assessments", sa.Column("consultation_details", sa.Text(), nullable=True)
    )
    op.add_column(
        "assessment_responses", sa.Column("comment", sa.Text(), nullable=True)
    )

    op.execute(
        "UPDATE assessments SET consultation_interest = false WHERE consultation_interest IS NULL"
    )

    op.alter_column(
        "assessments",
        "consultation_interest",
        nullable=False,
        server_default=sa.text("false"),
    )


def downgrade() -> None:
    op.drop_column("assessment_responses", "comment")
    op.drop_column("assessments", "consultation_details")
    op.drop_column("assessments", "consultation_interest")
