"""add unique constraint on assessment_id and report_type for reports

Revision ID: 1761546662
Revises: 1760707473
Create Date: 2025-10-27 00:00:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "1761546662"
down_revision = "1760707473"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DELETE FROM reports
        WHERE id IN (
            SELECT id FROM (
                SELECT id,
                       ROW_NUMBER() OVER (
                           PARTITION BY assessment_id, report_type
                           ORDER BY requested_at DESC
                       ) as rn
                FROM reports
            ) t
            WHERE t.rn > 1
        )
    """
    )

    op.create_unique_constraint(
        "uq_reports_assessment_type",
        "reports",
        ["assessment_id", "report_type"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_reports_assessment_type",
        "reports",
        type_="unique",
    )
