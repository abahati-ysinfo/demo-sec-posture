from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings


def get_limiter() -> Limiter:
    if not settings.RATE_LIMIT_ENABLED:
        limiter = Limiter(
            key_func=get_remote_address,
            storage_uri="memory://",
            default_limits=[],
            headers_enabled=False,
            enabled=False,
        )
        return limiter

    storage_uri = settings.REDIS_URL if settings.REDIS_URL else "memory://"

    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=storage_uri,
        default_limits=["100/minute"],
        headers_enabled=True,
    )

    return limiter


limiter = get_limiter()
