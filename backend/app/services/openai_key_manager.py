"""OpenAI API Key Manager for round-robin key rotation and management."""

import logging
from datetime import UTC, datetime, timedelta
from types import TracebackType
from typing import Self

from openai import OpenAI
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.openai_key import OpenAIAPIKey
from app.utils.encryption import decrypt_api_key, encrypt_api_key, mask_api_key

logger = logging.getLogger(__name__)


class OpenAIKeyManager:
    """Manages OpenAI API keys with round-robin rotation and error handling."""

    def __init__(self, db: Session | None = None):
        """Initialize the key manager.

        Args:
            db: Optional database session. If not provided, creates a new one.
        """
        self.db = db
        self._owns_session = db is None
        if self._owns_session:
            self.db = SessionLocal()

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit - close session if we own it."""
        if self._owns_session and self.db:
            self.db.close()

    def add_key(self, key_name: str, api_key: str, created_by: str) -> OpenAIAPIKey:
        """Add a new OpenAI API key to the database.

        Args:
            key_name: Friendly name for the key
            api_key: The actual OpenAI API key
            created_by: Email of the admin who added the key

        Returns:
            The created OpenAIAPIKey object
        """
        assert self.db is not None
        encrypted_key = encrypt_api_key(api_key)

        key_obj = OpenAIAPIKey(
            key_name=key_name,
            encrypted_key=encrypted_key,
            is_active=True,
            created_by=created_by,
        )

        self.db.add(key_obj)
        self.db.commit()
        self.db.refresh(key_obj)

        logger.info(f"Added new OpenAI API key: {key_name} (ID: {key_obj.id})")
        return key_obj

    def list_keys(self, include_inactive: bool = False) -> list[dict]:
        """List all API keys with masked values.

        Args:
            include_inactive: Whether to include inactive keys

        Returns:
            List of key information dictionaries with masked keys
        """
        assert self.db is not None
        query = self.db.query(OpenAIAPIKey)

        if not include_inactive:
            query = query.filter(OpenAIAPIKey.is_active)

        keys = query.order_by(OpenAIAPIKey.created_at.desc()).all()

        result = []
        for key in keys:
            decrypted_key = decrypt_api_key(str(key.encrypted_key))
            result.append(
                {
                    "id": key.id,
                    "key_name": key.key_name,
                    "masked_key": mask_api_key(decrypted_key),
                    "is_active": key.is_active,
                    "last_used_at": key.last_used_at,
                    "usage_count": key.usage_count,
                    "cooldown_until": key.cooldown_until,
                    "error_count": key.error_count,
                    "created_at": key.created_at,
                    "created_by": key.created_by,
                }
            )

        return result

    def get_next_key(self) -> tuple[str, str]:
        """Get the next available API key using round-robin (LRU) selection.

        Returns:
            Tuple of (key_id, decrypted_api_key)

        Raises:
            ValueError: If no active keys are available
        """
        assert self.db is not None
        now = datetime.now(UTC)

        query = (
            self.db.query(OpenAIAPIKey)
            .filter(
                and_(
                    OpenAIAPIKey.is_active,
                    (OpenAIAPIKey.cooldown_until.is_(None))
                    | (OpenAIAPIKey.cooldown_until <= now),
                )
            )
            .order_by(
                OpenAIAPIKey.cooldown_until.nulls_first(),
                OpenAIAPIKey.last_used_at.nulls_first(),
                OpenAIAPIKey.usage_count.asc(),
                OpenAIAPIKey.created_at.asc(),
            )
        )

        key = query.first()

        if not key:
            raise ValueError(
                "No active OpenAI API keys available. "
                "Please add API keys in the admin portal."
            )

        key.last_used_at = now  # type: ignore[assignment]
        key.usage_count += 1  # type: ignore[assignment]
        self.db.commit()

        decrypted_key = decrypt_api_key(str(key.encrypted_key))
        logger.info(
            f"Selected API key: {key.key_name} (ID: {key.id}, usage: {key.usage_count})"
        )

        return (str(key.id), decrypted_key)

    def record_success(self, key_id: str) -> None:
        """Record a successful API call for a key.

        Args:
            key_id: The ID of the key that was used successfully
        """
        assert self.db is not None
        key = self.db.query(OpenAIAPIKey).filter(OpenAIAPIKey.id == key_id).first()
        if key:
            key.error_count = 0  # type: ignore[assignment]
            key.cooldown_until = None  # type: ignore[assignment]
            self.db.commit()
            logger.debug(f"Recorded success for key: {key.key_name}")

    def record_failure(self, key_id: str, error: Exception) -> None:
        """Record a failed API call for a key and apply cooldown if needed.

        Args:
            key_id: The ID of the key that failed
            error: The exception that occurred
        """
        assert self.db is not None
        key = self.db.query(OpenAIAPIKey).filter(OpenAIAPIKey.id == key_id).first()
        if not key:
            return

        key.error_count += 1  # type: ignore[assignment]

        error_str = str(error).lower()
        is_rate_limit = "429" in error_str or "rate limit" in error_str

        if is_rate_limit:
            cooldown_minutes = min(2 ** int(key.error_count), 60)  # Max 60 minutes
            key.cooldown_until = datetime.now(UTC) + timedelta(minutes=cooldown_minutes)  # type: ignore[assignment]
            logger.warning(
                f"Rate limit hit for key {key.key_name}. "
                f"Cooldown until {key.cooldown_until} ({cooldown_minutes} minutes)"
            )
        elif key.error_count >= 5:
            key.is_active = False  # type: ignore[assignment]
            logger.error(
                f"Key {key.key_name} deactivated after {key.error_count} consecutive errors"
            )

        self.db.commit()

    def toggle_key(self, key_id: str, is_active: bool) -> OpenAIAPIKey:
        """Toggle a key's active status.

        Args:
            key_id: The ID of the key to toggle
            is_active: The new active status

        Returns:
            The updated OpenAIAPIKey object

        Raises:
            ValueError: If key not found
        """
        assert self.db is not None
        key = self.db.query(OpenAIAPIKey).filter(OpenAIAPIKey.id == key_id).first()
        if not key:
            raise ValueError(f"API key not found: {key_id}")

        key.is_active = is_active  # type: ignore[assignment]
        if is_active:
            key.error_count = 0  # type: ignore[assignment]
            key.cooldown_until = None  # type: ignore[assignment]

        self.db.commit()
        self.db.refresh(key)

        logger.info(
            f"Toggled key {key.key_name} to {'active' if is_active else 'inactive'}"
        )
        return key

    def delete_key(self, key_id: str) -> None:
        """Delete an API key.

        Args:
            key_id: The ID of the key to delete

        Raises:
            ValueError: If key not found
        """
        assert self.db is not None
        key = self.db.query(OpenAIAPIKey).filter(OpenAIAPIKey.id == key_id).first()
        if not key:
            raise ValueError(f"API key not found: {key_id}")

        key_name = key.key_name
        self.db.delete(key)
        self.db.commit()

        logger.info(f"Deleted API key: {key_name} (ID: {key_id})")

    def test_key(self, api_key: str) -> tuple[bool, str]:
        """Test if an API key is valid by making a small API call.

        Args:
            api_key: The API key to test

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            client = OpenAI(api_key=api_key, timeout=10.0)

            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
            )

            if response and response.choices:
                return (True, "API key is valid")
            else:
                return (False, "API key test failed: No response from OpenAI")

        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid" in error_msg.lower():
                return (False, "API key is invalid or unauthorized")
            elif "403" in error_msg or "model_not_found" in error_msg.lower():
                return (
                    False,
                    f"API key is valid but does not have access to model '{settings.OPENAI_MODEL}'",
                )
            elif "429" in error_msg:
                return (False, "API key is valid but rate limited")
            else:
                return (False, f"API key test failed: {error_msg}")


def get_openai_client_with_rotation(db: Session | None = None) -> tuple[OpenAI, str]:
    """Get an OpenAI client with a rotated API key.

    Args:
        db: Optional database session

    Returns:
        Tuple of (OpenAI client, key_id)

    Raises:
        ValueError: If no active keys are available
    """
    with OpenAIKeyManager(db) as manager:
        key_id, api_key = manager.get_next_key()

        client = OpenAI(api_key=api_key, timeout=settings.OPENAI_TIMEOUT)

        return (client, key_id)
