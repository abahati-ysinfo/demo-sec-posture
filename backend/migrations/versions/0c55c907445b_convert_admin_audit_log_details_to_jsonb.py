"""convert admin audit log details to jsonb

Revision ID: 0c55c907445b
Revises: 6a3e3285b47f
Create Date: 2025-09-18 00:11:41.882971

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0c55c907445b"
down_revision = "6a3e3285b47f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        DECLARE
            log_record RECORD;
        BEGIN
            FOR log_record IN
                SELECT id, details
                FROM admin_audit_log
                WHERE details IS NOT NULL
            LOOP
                BEGIN
                    PERFORM log_record.details::jsonb;
                EXCEPTION
                    WHEN others THEN
                        UPDATE admin_audit_log
                        SET details = to_jsonb(log_record.details)::text
                        WHERE id = log_record.id;
                END;
            END LOOP;
        END;
        $$;
        """
    )
    op.execute(
        "ALTER TABLE admin_audit_log ALTER COLUMN details TYPE JSONB USING details::jsonb"
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE admin_audit_log
        ALTER COLUMN details TYPE TEXT
        USING (
            CASE
                WHEN details IS NULL THEN NULL
                WHEN jsonb_typeof(details) = 'string' THEN jsonb_build_array(details)->>0
                ELSE details::text
            END
        )
        """
    )
