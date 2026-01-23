"""Datetime utility functions for timezone handling."""

from datetime import UTC, datetime


def to_utc_aware(dt: datetime | None) -> datetime | None:
    """
    Convert a naive datetime to UTC-aware datetime.

    This helper ensures all datetime objects are timezone-aware before
    performing arithmetic operations. SQLite in tests returns naive datetimes
    even when columns are marked as DateTime(timezone=True).

    Args:
        dt: A datetime object (naive or aware) or None

    Returns:
        A timezone-aware datetime in UTC, or None if input is None

    Note:
        This assumes naive datetimes are in UTC, which is true for this
        application since we historically used datetime.utcnow().
    """
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)
