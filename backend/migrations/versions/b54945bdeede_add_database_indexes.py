"""add_database_indexes

Revision ID: b54945bdeede
Revises: 9cbe6669eb84
Create Date: 2025-10-06 06:09:50.197284

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "b54945bdeede"
down_revision = "9cbe6669eb84"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_assessments_user_id", "assessments", ["user_id"])
    op.create_index("ix_assessments_status", "assessments", ["status"])
    op.create_index(
        "ix_assessment_responses_assessment_id_section_id",
        "assessment_responses",
        ["assessment_id", "section_id"],
    )
    op.create_index("ix_reports_assessment_id", "reports", ["assessment_id"])
    op.create_index("ix_reports_status", "reports", ["status"])


def downgrade() -> None:
    op.drop_index("ix_reports_status", table_name="reports")
    op.drop_index("ix_reports_assessment_id", table_name="reports")
    op.drop_index(
        "ix_assessment_responses_assessment_id_section_id",
        table_name="assessment_responses",
    )
    op.drop_index("ix_assessments_status", table_name="assessments")
    op.drop_index("ix_assessments_user_id", table_name="assessments")
