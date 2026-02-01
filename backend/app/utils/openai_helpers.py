"""OpenAI API helper utilities for handling different model versions."""

import re
from typing import Any

from app.core.config import settings

# Models that use the older max_tokens parameter
# These are legacy models - newer models use max_completion_tokens
LEGACY_MAX_TOKENS_MODELS = [
    r"^gpt-3\.5",  # gpt-3.5-turbo and variants
    r"^gpt-4(?!o)",  # gpt-4, gpt-4-turbo, but NOT gpt-4o (which uses new params)
    r"^text-davinci",  # Legacy completion models
    r"^davinci",
    r"^curie",
    r"^babbage",
    r"^ada",
]


def uses_legacy_max_tokens(model: str) -> bool:
    """Check if a model uses the legacy max_tokens parameter.

    Args:
        model: The OpenAI model name

    Returns:
        True if the model uses max_tokens, False if it uses max_completion_tokens
    """
    model_lower = model.lower()
    for pattern in LEGACY_MAX_TOKENS_MODELS:
        if re.match(pattern, model_lower):
            return True
    return False


def get_token_params(max_tokens: int, model: str | None = None) -> dict[str, Any]:
    """Get the appropriate token parameter based on the model.

    Automatically detects whether to use 'max_tokens' (legacy) or 'max_completion_tokens'
    (newer models like gpt-4o, gpt-5, o1, o3, etc.) based on the model name.

    This allows changing the OPENAI_MODEL environment variable without needing
    to update any code - the system will automatically use the correct parameter.

    Args:
        max_tokens: The maximum number of tokens to generate
        model: Optional model name. If not provided, uses settings.OPENAI_MODEL

    Returns:
        Dictionary with the appropriate token parameter
    """
    model_name = model or settings.OPENAI_MODEL

    if uses_legacy_max_tokens(model_name):
        return {"max_tokens": max_tokens}

    # Default to max_completion_tokens for newer/unknown models
    # This is future-proof as OpenAI is moving towards this parameter
    return {"max_completion_tokens": max_tokens}
