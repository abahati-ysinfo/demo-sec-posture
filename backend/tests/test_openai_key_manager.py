"""Tests for OpenAI API key management functionality."""

from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from app.models.openai_key import OpenAIAPIKey
from app.services.openai_key_manager import OpenAIKeyManager
from app.utils.encryption import decrypt_api_key, encrypt_api_key, mask_api_key


@pytest.fixture
def db_session(mocker: Any) -> Any:
    """Mock database session."""
    session = mocker.MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    session.query.return_value.filter.return_value.order_by.return_value.first.return_value = None
    session.query.return_value.filter.return_value.all.return_value = []
    return session


@pytest.fixture
def key_manager(db_session: Any) -> Any:
    """Create OpenAIKeyManager instance with mocked session."""
    return OpenAIKeyManager(db_session)


class TestEncryption:
    """Test encryption utilities."""

    def test_encrypt_decrypt_roundtrip(self, encryption_key: Any) -> None:
        """Test that encryption and decryption work correctly."""
        original_key = "sk-test1234567890abcdefghijklmnopqrstuvwxyz"
        encrypted = encrypt_api_key(original_key)
        decrypted = decrypt_api_key(encrypted)

        assert decrypted == original_key
        assert encrypted != original_key

    def test_mask_api_key(self) -> None:
        """Test API key masking."""
        api_key = "sk-test1234567890abcdefghijklmnopqrstuvwxyz"
        masked = mask_api_key(api_key)

        assert masked.startswith("sk-...")
        assert masked.endswith(api_key[-4:])
        assert len(masked) < len(api_key)

    def test_mask_short_key(self) -> None:
        """Test masking of short API keys."""
        api_key = "sk-123"
        masked = mask_api_key(api_key)

        assert masked.startswith("***")


class TestOpenAIKeyManager:
    """Test OpenAIKeyManager service."""

    def test_add_key_success(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test adding a new API key."""
        key = key_manager.add_key(
            key_name="Test Key",
            api_key="sk-test1234567890",
            created_by="admin@test.com",
        )

        assert key.key_name == "Test Key"
        assert key.is_active is True
        assert key.created_by == "admin@test.com"
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()

    def test_add_key_invalid(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test that test_key method can validate keys."""
        with patch("app.services.openai_key_manager.OpenAI") as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception(
                "Invalid API key"
            )

            is_valid, message = key_manager.test_key("sk-invalid")

            assert is_valid is False
            assert "invalid" in message.lower()

    def test_list_keys_active_only(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test listing only active keys."""
        mock_key1 = Mock(spec=OpenAIAPIKey)
        mock_key1.id = "key1"
        mock_key1.key_name = "Key 1"
        mock_key1.encrypted_key = encrypt_api_key("sk-test1")
        mock_key1.is_active = True
        mock_key1.last_used_at = None
        mock_key1.usage_count = 5
        mock_key1.cooldown_until = None
        mock_key1.error_count = 0
        mock_key1.created_at = datetime.now(UTC)
        mock_key1.created_by = "admin@test.com"

        mock_key2 = Mock(spec=OpenAIAPIKey)
        mock_key2.id = "key2"
        mock_key2.key_name = "Key 2"
        mock_key2.encrypted_key = encrypt_api_key("sk-test2")
        mock_key2.is_active = False
        mock_key2.last_used_at = None
        mock_key2.usage_count = 0
        mock_key2.cooldown_until = None
        mock_key2.error_count = 0
        mock_key2.created_at = datetime.now(UTC)
        mock_key2.created_by = "admin@test.com"

        db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
            mock_key1
        ]

        keys = key_manager.list_keys(include_inactive=False)

        assert len(keys) == 1
        assert keys[0]["id"] == "key1"
        assert keys[0]["key_name"] == "Key 1"
        assert keys[0]["is_active"] is True
        assert "sk-..." in keys[0]["masked_key"]

    def test_list_keys_include_inactive(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test listing all keys including inactive."""
        mock_key1 = Mock(spec=OpenAIAPIKey)
        mock_key1.id = "key1"
        mock_key1.key_name = "Key 1"
        mock_key1.encrypted_key = encrypt_api_key("sk-test1")
        mock_key1.is_active = True
        mock_key1.last_used_at = None
        mock_key1.usage_count = 5
        mock_key1.cooldown_until = None
        mock_key1.error_count = 0
        mock_key1.created_at = datetime.now(UTC)
        mock_key1.created_by = "admin@test.com"

        mock_key2 = Mock(spec=OpenAIAPIKey)
        mock_key2.id = "key2"
        mock_key2.key_name = "Key 2"
        mock_key2.encrypted_key = encrypt_api_key("sk-test2")
        mock_key2.is_active = False
        mock_key2.last_used_at = None
        mock_key2.usage_count = 0
        mock_key2.cooldown_until = None
        mock_key2.error_count = 0
        mock_key2.created_at = datetime.now(UTC)
        mock_key2.created_by = "admin@test.com"

        db_session.query.return_value.order_by.return_value.all.return_value = [
            mock_key1,
            mock_key2,
        ]

        keys = key_manager.list_keys(include_inactive=True)

        assert len(keys) == 2
        assert keys[0]["id"] == "key1"
        assert keys[1]["id"] == "key2"

    def test_get_next_key_lru_selection(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test LRU key selection."""
        now = datetime.now(UTC)

        mock_key1 = Mock(spec=OpenAIAPIKey)
        mock_key1.id = "key1"
        mock_key1.encrypted_key = encrypt_api_key("sk-test1")
        mock_key1.last_used_at = now - timedelta(hours=2)
        mock_key1.usage_count = 10
        mock_key1.cooldown_until = None

        mock_key2 = Mock(spec=OpenAIAPIKey)
        mock_key2.id = "key2"
        mock_key2.encrypted_key = encrypt_api_key("sk-test2")
        mock_key2.last_used_at = now - timedelta(hours=1)
        mock_key2.usage_count = 5
        mock_key2.cooldown_until = None

        db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key1

        key_id, api_key = key_manager.get_next_key()

        assert key_id == "key1"
        assert api_key == "sk-test1"
        assert mock_key1.usage_count == 11
        assert mock_key1.last_used_at is not None
        db_session.commit.assert_called()

    def test_get_next_key_no_keys_available(
        self, key_manager: Any, db_session: Any
    ) -> None:
        """Test error when no keys are available."""
        db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

        with pytest.raises(ValueError, match="No active OpenAI API keys available"):
            key_manager.get_next_key()

    def test_get_next_key_skip_cooldown(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test that keys in cooldown are skipped."""
        now = datetime.now(UTC)

        mock_key1 = Mock(spec=OpenAIAPIKey)
        mock_key1.id = "key1"
        mock_key1.encrypted_key = encrypt_api_key("sk-test1")
        mock_key1.cooldown_until = now + timedelta(minutes=5)

        mock_key2 = Mock(spec=OpenAIAPIKey)
        mock_key2.id = "key2"
        mock_key2.encrypted_key = encrypt_api_key("sk-test2")
        mock_key2.cooldown_until = None
        mock_key2.last_used_at = None
        mock_key2.usage_count = 0

        db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key2

        key_id, api_key = key_manager.get_next_key()

        assert key_id == "key2"
        assert api_key == "sk-test2"

    def test_record_success(self, key_manager: Any, db_session: Any) -> None:
        """Test recording successful API call."""
        mock_key = Mock(spec=OpenAIAPIKey)
        mock_key.error_count = 3
        mock_key.cooldown_until = datetime.now(UTC) + timedelta(minutes=5)

        db_session.query.return_value.filter.return_value.first.return_value = mock_key

        key_manager.record_success("key1")

        assert mock_key.error_count == 0
        assert mock_key.cooldown_until is None
        db_session.commit.assert_called_once()

    def test_record_failure_rate_limit(self, key_manager: Any, db_session: Any) -> None:
        """Test recording rate limit failure with exponential backoff."""
        mock_key = Mock(spec=OpenAIAPIKey)
        mock_key.id = "key1"
        mock_key.key_name = "Test Key"
        mock_key.error_count = 2
        mock_key.is_active = True

        db_session.query.return_value.filter.return_value.first.return_value = mock_key

        error = Exception("Rate limit exceeded")
        error.status_code = 429  # type: ignore[attr-defined]

        key_manager.record_failure("key1", error)

        assert mock_key.error_count == 3
        assert mock_key.cooldown_until is not None
        db_session.commit.assert_called()

    def test_record_failure_auto_deactivate(
        self, key_manager: Any, db_session: Any
    ) -> None:
        """Test auto-deactivation after 5 consecutive errors."""
        mock_key = Mock(spec=OpenAIAPIKey)
        mock_key.id = "key1"
        mock_key.key_name = "Test Key"
        mock_key.error_count = 4
        mock_key.is_active = True

        db_session.query.return_value.filter.return_value.first.return_value = mock_key

        error = Exception("Connection timeout")

        key_manager.record_failure("key1", error)

        assert mock_key.error_count == 5
        assert mock_key.is_active is False
        db_session.commit.assert_called()

    def test_toggle_key_activate(self, key_manager: Any, db_session: Any) -> None:
        """Test activating a key."""
        mock_key = Mock(spec=OpenAIAPIKey)
        mock_key.is_active = False

        db_session.query.return_value.filter.return_value.first.return_value = mock_key

        key_manager.toggle_key("key1", True)

        assert mock_key.is_active is True
        db_session.commit.assert_called_once()

    def test_toggle_key_deactivate(self, key_manager: Any, db_session: Any) -> None:
        """Test deactivating a key."""
        mock_key = Mock(spec=OpenAIAPIKey)
        mock_key.is_active = True

        db_session.query.return_value.filter.return_value.first.return_value = mock_key

        key_manager.toggle_key("key1", False)

        assert mock_key.is_active is False
        db_session.commit.assert_called_once()

    def test_toggle_key_not_found(self, key_manager: Any, db_session: Any) -> None:
        """Test toggling non-existent key."""
        db_session.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError, match="API key not found"):
            key_manager.toggle_key("nonexistent", True)

    def test_delete_key(self, key_manager: Any, db_session: Any) -> None:
        """Test deleting a key."""
        mock_key = Mock(spec=OpenAIAPIKey)

        db_session.query.return_value.filter.return_value.first.return_value = mock_key

        key_manager.delete_key("key1")

        db_session.delete.assert_called_once_with(mock_key)
        db_session.commit.assert_called_once()

    def test_delete_key_not_found(self, key_manager: Any, db_session: Any) -> None:
        """Test deleting non-existent key."""
        db_session.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError, match="API key not found"):
            key_manager.delete_key("nonexistent")

    @patch("app.services.openai_key_manager.OpenAI")
    def test_test_key_valid(self, mock_openai_class: Any, key_manager: Any) -> None:
        """Test validating a valid API key."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response

        is_valid, message = key_manager.test_key("sk-valid-key")

        assert is_valid is True
        assert "valid" in message.lower()

    @patch("app.services.openai_key_manager.OpenAI")
    def test_test_key_invalid(self, mock_openai_class: Any, key_manager: Any) -> None:
        """Test validating an invalid API key."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_client.chat.completions.create.side_effect = Exception("Invalid API key")

        is_valid, message = key_manager.test_key("sk-invalid-key")

        assert is_valid is False
        assert "invalid" in message.lower()

    def test_context_manager(self, db_session: Any) -> None:
        """Test OpenAIKeyManager as context manager."""
        with OpenAIKeyManager(db_session) as manager:
            assert manager.db == db_session
            assert manager._owns_session is False

        db_session.close.assert_not_called()


class TestKeyRotationScenarios:
    """Test real-world key rotation scenarios."""

    def test_round_robin_with_three_keys(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test round-robin rotation with three keys."""
        now = datetime.now(UTC)

        keys = []
        for i in range(3):
            mock_key = Mock(spec=OpenAIAPIKey)
            mock_key.id = f"key{i + 1}"
            mock_key.encrypted_key = encrypt_api_key(f"sk-test{i + 1}")
            mock_key.last_used_at = now - timedelta(hours=3 - i)
            mock_key.usage_count = i * 5
            mock_key.cooldown_until = None
            keys.append(mock_key)

        call_count = 0

        def mock_query_side_effect(*args: Any, **kwargs: Any) -> Any:
            nonlocal call_count
            result = Mock()
            result.filter.return_value.order_by.return_value.first.return_value = keys[
                call_count % 3
            ]
            call_count += 1
            return result

        db_session.query.side_effect = mock_query_side_effect

        selected_keys = []
        for _ in range(3):
            key_id, _ = key_manager.get_next_key()
            selected_keys.append(key_id)

        assert len(set(selected_keys)) == 3

    def test_recovery_after_cooldown(
        self, encryption_key: Any, key_manager: Any, db_session: Any
    ) -> None:
        """Test that keys become available after cooldown expires."""
        now = datetime.now(UTC)

        mock_key = Mock(spec=OpenAIAPIKey)
        mock_key.id = "key1"
        mock_key.encrypted_key = encrypt_api_key("sk-test1")
        mock_key.cooldown_until = now - timedelta(seconds=1)
        mock_key.last_used_at = None
        mock_key.usage_count = 0

        db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key

        key_id, api_key = key_manager.get_next_key()

        assert key_id == "key1"
        assert api_key == "sk-test1"
