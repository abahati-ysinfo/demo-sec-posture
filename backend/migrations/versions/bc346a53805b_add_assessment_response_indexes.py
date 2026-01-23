"""add_assessment_response_indexes

Revision ID: bc346a53805b
Revises: 1761546662
Create Date: 2025-10-28 00:27:31.434364

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "bc346a53805b"
down_revision = "1761546662"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "idx_assessment_responses_assessment_question",
        "assessment_responses",
        ["assessment_id", "question_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "idx_assessment_responses_assessment_id",
        "assessment_responses",
        ["assessment_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "idx_assessment_responses_updated_at",
        "assessment_responses",
        ["updated_at"],
        unique=False,
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_index(
        "idx_assessment_responses_updated_at", table_name="assessment_responses"
    )
    op.drop_index(
        "idx_assessment_responses_assessment_id", table_name="assessment_responses"
    )
    op.drop_index(
        "idx_assessment_responses_assessment_question",
        table_name="assessment_responses",
    )
