import json
import logging
import os
from typing import Any

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self) -> None:
        self._redis_client: redis.Redis | None = None
        self._questions_file_mtime: float | None = None
        self._initialize_redis()

    def _initialize_redis(self) -> None:
        if not settings.REDIS_URL:
            logger.warning("REDIS_URL not configured. Caching disabled.")
            return

        try:
            self._redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
            self._redis_client.ping()
            logger.info("Redis cache connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}. Caching disabled.")
            self._redis_client = None

    def _is_available(self) -> bool:
        if self._redis_client is None:
            return False
        try:
            self._redis_client.ping()
            return True
        except Exception:
            return False

    def get(self, key: str) -> Any | None:
        if not self._is_available():
            return None

        try:
            assert self._redis_client is not None
            value = self._redis_client.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                if isinstance(value, bytes):
                    return json.loads(value.decode("utf-8"))
                return json.loads(str(value))
            logger.debug(f"Cache miss: {key}")
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        if not self._is_available():
            return False

        try:
            assert self._redis_client is not None
            serialized = json.dumps(value)
            if ttl:
                self._redis_client.setex(key, ttl, serialized)
            else:
                self._redis_client.set(key, serialized)
            logger.debug(f"Cache set: {key} (TTL: {ttl})")
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        if not self._is_available():
            return False

        try:
            assert self._redis_client is not None
            self._redis_client.delete(key)
            logger.debug(f"Cache delete: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False

    def clear(self) -> bool:
        if not self._is_available():
            return False

        try:
            assert self._redis_client is not None
            self._redis_client.flushdb()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False

    def get_questions_file_path(self) -> str:
        current_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        return os.path.join(current_dir, "data", "security_assessment_questions.md")

    def has_questions_file_changed(self) -> bool:
        questions_file = self.get_questions_file_path()

        if not os.path.exists(questions_file):
            return True

        current_mtime = os.path.getmtime(questions_file)

        if self._questions_file_mtime is None:
            self._questions_file_mtime = current_mtime
            return True

        if current_mtime > self._questions_file_mtime:
            self._questions_file_mtime = current_mtime
            logger.info("Questions file has been modified, invalidating cache")
            return True

        return False


cache_service = CacheService()
