import logging
import time

import sentry_sdk
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

SLOW_QUERY_THRESHOLD = 100

engine = create_engine(
    settings.DATABASE_URL or "",
    connect_args={"check_same_thread": False}
    if settings.DATABASE_URL and "sqlite" in settings.DATABASE_URL
    else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(
    conn: object,
    cursor: object,
    statement: object,
    parameters: object,
    context: object,
    executemany: object,
) -> None:
    conn.info.setdefault("query_start_time", []).append(time.time())  # type: ignore[attr-defined]


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(
    conn: object,
    cursor: object,
    statement: object,
    parameters: object,
    context: object,
    executemany: object,
) -> None:
    total_time = time.time() - conn.info["query_start_time"].pop()  # type: ignore[attr-defined]
    duration_ms = total_time * 1000

    if duration_ms > SLOW_QUERY_THRESHOLD:
        logger.warning(f"Slow query ({duration_ms:.2f}ms): {str(statement)[:200]}")  # type: ignore[index]
        if settings.SENTRY_DSN:
            sentry_sdk.capture_message(
                f"Slow database query: {duration_ms:.2f}ms",
                level="warning",
                extras={"query": str(statement)[:500], "duration_ms": duration_ms},  # type: ignore[dict-item]
            )


def get_db() -> object:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
