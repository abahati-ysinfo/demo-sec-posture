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

# Models that support custom temperature values
# Newer reasoning models (o1, o3, gpt-5-nano, etc.) only support temperature=1
MODELS_SUPPORTING_CUSTOM_TEMPERATURE = [
    r"^gpt-3\.5",  # gpt-3.5-turbo and variants
    r"^gpt-4",  # gpt-4, gpt-4-turbo, gpt-4o
    r"^text-davinci",
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


def supports_custom_temperature(model: str) -> bool:
    """Check if a model supports custom temperature values.

    Some newer models (o1, o3, gpt-5-nano, etc.) only support temperature=1.

    Args:
        model: The OpenAI model name

    Returns:
        True if the model supports custom temperature, False otherwise
    """
    model_lower = model.lower()
    for pattern in MODELS_SUPPORTING_CUSTOM_TEMPERATURE:
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


def get_temperature_param(
    temperature: float, model: str | None = None
) -> dict[str, Any]:
    """Get the temperature parameter if supported by the model.

    Some newer models (o1, o3, gpt-5-nano, etc.) only support temperature=1.
    For these models, we omit the temperature parameter entirely.

    Args:
        temperature: The desired temperature value
        model: Optional model name. If not provided, uses settings.OPENAI_MODEL

    Returns:
        Dictionary with temperature parameter if supported, empty dict otherwise
    """
    model_name = model or settings.OPENAI_MODEL

    if supports_custom_temperature(model_name):
        return {"temperature": temperature}

    # For models that don't support custom temperature, omit the parameter
    # (they will use their default, typically 1)
    return {}
