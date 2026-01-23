from typing import Any
from unittest.mock import MagicMock, patch

import redis

from app.services.cache import CacheService


class TestCacheService:
    """Tests for CacheService Redis caching functionality"""

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_init_with_valid_redis_url(
        self, mock_from_url: Any, mock_settings: Any
    ) -> None:
        """Test successful Redis initialization with valid URL"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        cache = CacheService()

        mock_from_url.assert_called_once_with(
            "redis://localhost:6379/0",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        mock_redis.ping.assert_called_once()
        assert cache._redis_client == mock_redis

    @patch("app.services.cache.settings")
    def test_init_without_redis_url(self, mock_settings: Any) -> None:
        """Test graceful handling when REDIS_URL not configured"""
        mock_settings.REDIS_URL = None

        cache = CacheService()

        assert cache._redis_client is None

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_init_with_connection_failure(
        self, mock_from_url: Any, mock_settings: Any
    ) -> None:
        """Test graceful handling when Redis connection fails"""
        mock_settings.REDIS_URL = "redis://invalid:6379/0"
        mock_redis = MagicMock()
        mock_redis.ping.side_effect = redis.ConnectionError("Connection failed")
        mock_from_url.return_value = mock_redis

        cache = CacheService()

        assert cache._redis_client is None

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_is_available_when_redis_connected(
        self, mock_from_url: Any, mock_settings: Any
    ) -> None:
        """Test _is_available returns True when Redis is connected"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        cache = CacheService()

        assert cache._is_available() is True
        mock_redis.ping.assert_called()

    @patch("app.services.cache.settings")
    def test_is_available_when_redis_not_initialized(self, mock_settings: Any) -> None:
        """Test _is_available returns False when Redis not initialized"""
        mock_settings.REDIS_URL = None

        cache = CacheService()

        assert cache._is_available() is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_is_available_when_redis_ping_fails(
        self, mock_from_url: Any, mock_settings: Any
    ) -> None:
        """Test _is_available returns False when ping fails"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        cache = CacheService()

        mock_redis.ping.side_effect = redis.ConnectionError("Connection lost")

        assert cache._is_available() is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_get_cache_hit(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test get() returns cached value on cache hit"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_redis.get.return_value = '{"key": "value"}'
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.get("test_key")

        assert result == {"key": "value"}
        mock_redis.get.assert_called_once_with("test_key")

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_get_cache_miss(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test get() returns None on cache miss"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_redis.get.return_value = None
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.get("test_key")

        assert result is None
        mock_redis.get.assert_called_once_with("test_key")

    @patch("app.services.cache.settings")
    def test_get_when_redis_unavailable(self, mock_settings: Any) -> None:
        """Test get() returns None when Redis unavailable"""
        mock_settings.REDIS_URL = None

        cache = CacheService()
        result = cache.get("test_key")

        assert result is None

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_get_with_error(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test get() handles Redis errors gracefully"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_redis.get.side_effect = redis.RedisError("Redis error")
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.get("test_key")

        assert result is None

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_set_without_ttl(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test set() stores value without TTL"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.set("test_key", {"data": "value"})

        assert result is True
        mock_redis.set.assert_called_once_with("test_key", '{"data": "value"}')

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_set_with_ttl(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test set() stores value with TTL"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.set("test_key", {"data": "value"}, ttl=300)

        assert result is True
        mock_redis.setex.assert_called_once_with("test_key", 300, '{"data": "value"}')

    @patch("app.services.cache.settings")
    def test_set_when_redis_unavailable(self, mock_settings: Any) -> None:
        """Test set() returns False when Redis unavailable"""
        mock_settings.REDIS_URL = None

        cache = CacheService()
        result = cache.set("test_key", {"data": "value"})

        assert result is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_set_with_error(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test set() handles Redis errors gracefully"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_redis.set.side_effect = redis.RedisError("Redis error")
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.set("test_key", {"data": "value"})

        assert result is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_delete_success(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test delete() removes key from cache"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.delete("test_key")

        assert result is True
        mock_redis.delete.assert_called_once_with("test_key")

    @patch("app.services.cache.settings")
    def test_delete_when_redis_unavailable(self, mock_settings: Any) -> None:
        """Test delete() returns False when Redis unavailable"""
        mock_settings.REDIS_URL = None

        cache = CacheService()
        result = cache.delete("test_key")

        assert result is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_delete_with_error(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test delete() handles Redis errors gracefully"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_redis.delete.side_effect = redis.RedisError("Redis error")
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.delete("test_key")

        assert result is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_clear_success(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test clear() flushes all cache keys"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.clear()

        assert result is True
        mock_redis.flushdb.assert_called_once()

    @patch("app.services.cache.settings")
    def test_clear_when_redis_unavailable(self, mock_settings: Any) -> None:
        """Test clear() returns False when Redis unavailable"""
        mock_settings.REDIS_URL = None

        cache = CacheService()
        result = cache.clear()

        assert result is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.redis.from_url")
    def test_clear_with_error(self, mock_from_url: Any, mock_settings: Any) -> None:
        """Test clear() handles Redis errors gracefully"""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_redis = MagicMock()
        mock_redis.flushdb.side_effect = redis.RedisError("Redis error")
        mock_from_url.return_value = mock_redis

        cache = CacheService()
        result = cache.clear()

        assert result is False

    @patch("app.services.cache.settings")
    def test_get_questions_file_path(self, mock_settings: Any) -> None:
        """Test get_questions_file_path() returns correct path"""
        mock_settings.REDIS_URL = None

        cache = CacheService()
        path = cache.get_questions_file_path()

        assert path.endswith("data/security_assessment_questions.md")
        assert "backend" in path

    @patch("app.services.cache.settings")
    @patch("app.services.cache.os.path.exists")
    def test_has_questions_file_changed_file_not_exists(
        self, mock_exists: Any, mock_settings: Any
    ) -> None:
        """Test has_questions_file_changed() returns True when file doesn't exist"""
        mock_settings.REDIS_URL = None
        mock_exists.return_value = False

        cache = CacheService()
        result = cache.has_questions_file_changed()

        assert result is True

    @patch("app.services.cache.settings")
    @patch("app.services.cache.os.path.getmtime")
    @patch("app.services.cache.os.path.exists")
    def test_has_questions_file_changed_first_check(
        self, mock_exists: Any, mock_getmtime: Any, mock_settings: Any
    ) -> None:
        """Test has_questions_file_changed() returns True on first check"""
        mock_settings.REDIS_URL = None
        mock_exists.return_value = True
        mock_getmtime.return_value = 1234567890.0

        cache = CacheService()
        result = cache.has_questions_file_changed()

        assert result is True
        assert cache._questions_file_mtime == 1234567890.0

    @patch("app.services.cache.settings")
    @patch("app.services.cache.os.path.getmtime")
    @patch("app.services.cache.os.path.exists")
    def test_has_questions_file_changed_no_change(
        self, mock_exists: Any, mock_getmtime: Any, mock_settings: Any
    ) -> None:
        """Test has_questions_file_changed() returns False when file unchanged"""
        mock_settings.REDIS_URL = None
        mock_exists.return_value = True
        mock_getmtime.return_value = 1234567890.0

        cache = CacheService()
        cache.has_questions_file_changed()
        result = cache.has_questions_file_changed()

        assert result is False

    @patch("app.services.cache.settings")
    @patch("app.services.cache.os.path.getmtime")
    @patch("app.services.cache.os.path.exists")
    def test_has_questions_file_changed_file_modified(
        self, mock_exists: Any, mock_getmtime: Any, mock_settings: Any
    ) -> None:
        """Test has_questions_file_changed() returns True when file modified"""
        mock_settings.REDIS_URL = None
        mock_exists.return_value = True
        mock_getmtime.side_effect = [1234567890.0, 1234567900.0]

        cache = CacheService()
        cache.has_questions_file_changed()
        result = cache.has_questions_file_changed()

        assert result is True
        assert cache._questions_file_mtime == 1234567900.0
