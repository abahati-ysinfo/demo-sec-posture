"""
Scoring scales for weighted assessment scoring
"""

from typing import Any

SCALE_WEIGHTS: dict[str, dict[str, float]] = {
    "maturity": {
        "optimized": 1.0,
        "managed": 0.75,
        "defined": 0.5,
        "ad_hoc": 0.25,
        "ad-hoc": 0.25,
    },
    "frequency_review": {
        "quarterly": 1.0,
        "annually": 0.75,
        "only_after_changes": 0.5,
        "only_after_major_changes": 0.5,
        "as_needed": 0.5,
        "no_formal_review": 0.0,
        "never": 0.0,
    },
    "frequency_monitoring": {
        "continuously": 1.0,
        "daily": 0.9,
        "weekly": 0.8,
        "monthly": 0.7,
        "quarterly": 0.6,
        "only_when_issues": 0.3,
        "not_monitored": 0.0,
        "never": 0.0,
    },
    "coverage": {
        "76_100": 1.0,
        "51_75": 0.75,
        "26_50": 0.5,
        "0_25": 0.25,
    },
    "implementation": {
        "fully_implemented": 1.0,
        "partially_implemented": 0.5,
        "planned": 0.25,
        "not_implemented": 0.0,
    },
    "governance": {
        "documented_approved_maintained": 1.0,
        "documented_but_stale": 0.5,
        "informal_understanding": 0.25,
        "no_strategy": 0.0,
    },
}


def get_option_weight(scale_type: str, option_value: str) -> tuple[float, list[str]]:
    """
    Get weight and flags for an option value

    Returns:
        (weight_multiplier, flags)
    """
    flags: list[str] = []

    option_value_lower = option_value.lower().replace(" ", "_").replace("-", "_")

    if option_value_lower in ["unknown", "not_sure", "don't_know", "dont_know"]:
        return 0.0, ["unknown"]

    if option_value_lower in [
        "not_applicable",
        "n/a",
        "na",
        "not_applicable_to_our_organization",
    ]:
        return 0.0, ["not_applicable"]

    scale = SCALE_WEIGHTS.get(scale_type, {})
    weight = scale.get(option_value_lower, 1.0)

    return weight, flags


def normalize_option_value(value: str) -> str:
    """Normalize option value for consistent lookup"""
    normalized = value.lower().replace(" ", "_").replace("-", "_").replace("/", "_")

    if normalized in ["n_a", "na"]:
        return "not_applicable"

    return normalized


def map_numeric_to_slug(question: Any, answer_value: str) -> str:
    """
    Map numeric answer values to slugs based on question's current options.

    This handles legacy numeric values and in-progress assessments during migration.
    If answer_value is already a slug, returns it as-is.
    If answer_value is numeric, maps to the corresponding option slug by ordinal.

    Args:
        question: Question object with options list
        answer_value: The stored answer value (could be numeric "1" or slug "quarterly")

    Returns:
        Slug value for the answer
    """
    if not answer_value or not isinstance(answer_value, str):
        return answer_value

    if not answer_value.isdigit():
        return answer_value

    try:
        index = int(answer_value) - 1
        if 0 <= index < len(question.options):
            return str(question.options[index].value)
    except (ValueError, IndexError):
        pass

    return answer_value
