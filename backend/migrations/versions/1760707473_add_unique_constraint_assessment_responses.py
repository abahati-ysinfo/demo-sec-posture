"""add unique constraint on assessment_id and question_id

Revision ID: 1760707473
Revises: b54945bdeede
Create Date: 2025-10-17 00:00:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "1760707473"
down_revision = "b54945bdeede"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DELETE FROM assessment_responses
        WHERE id IN (
            SELECT id FROM (
                SELECT id,
                       ROW_NUMBER() OVER (
                           PARTITION BY assessment_id, question_id
                           ORDER BY updated_at DESC
                       ) as rn
                FROM assessment_responses
            ) t
            WHERE t.rn > 1
        )
    """
    )

    op.create_unique_constraint(
        "uq_assessment_responses_assessment_question",
        "assessment_responses",
        ["assessment_id", "question_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_assessment_responses_assessment_question",
        "assessment_responses",
        type_="unique",
    )
