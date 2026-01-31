"""OpenAI API helper utilities for handling different model versions."""

from typing import Any

from app.core.config import settings


def get_token_params(max_tokens: int) -> dict[str, Any]:
    """Get the appropriate token parameter based on model configuration.

    Newer OpenAI models (gpt-5, o1, etc.) use 'max_completion_tokens' instead of 'max_tokens'.
    This helper returns the correct parameter based on the OPENAI_USE_COMPLETION_TOKENS setting.

    Args:
        max_tokens: The maximum number of tokens to generate

    Returns:
        Dictionary with the appropriate token parameter
    """
    if settings.OPENAI_USE_COMPLETION_TOKENS:
        return {"max_completion_tokens": max_tokens}
    return {"max_tokens": max_tokens}
