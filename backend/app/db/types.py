"""Custom SQLAlchemy types for cross-database compatibility."""

from typing import Any

import sqlalchemy as sa
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator


class JSONBCompat(TypeDecorator):
    """
    Cross-database JSON type that uses JSONB on PostgreSQL and JSON on other databases.

    This allows models to use JSONB (which provides better indexing and performance on PostgreSQL)
    while maintaining compatibility with SQLite for testing.
    """

    impl = sa.JSON
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> sa.types.TypeEngine[Any]:
        """Load the appropriate JSON type based on the database dialect."""
        if dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import JSONB

            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(sa.JSON())
