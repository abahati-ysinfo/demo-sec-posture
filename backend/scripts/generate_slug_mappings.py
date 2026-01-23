"""
Generate slug mappings for all questions in security_assessment_questions.md

This script:
1. Parses all questions and their options
2. Generates stable slug identifiers for each option based on:
   - Scale type (if present): uses scale-appropriate slugs
   - Common patterns: yes/no, not_sure, not_applicable
   - Generic fallback: slugified label with uniqueness enforcement
3. Outputs JSON mapping: {question_id: {"1": "slug1", "2": "slug2", ...}}
4. Outputs CSV for human review

The generated mapping will be embedded in the Alembic migration script
to ensure reproducibility even if the markdown changes later.
"""

import json
import re
from pathlib import Path
from typing import Any

# Scale-appropriate slug mappings from scoring_scales.py
SCALE_SLUGS = {
    "maturity": ["optimized", "managed", "defined", "ad_hoc"],
    "governance": [
        "documented_approved_maintained",
        "documented_but_stale",
        "informal_understanding",
        "no_strategy",
    ],
    "frequency_review": [
        "quarterly",
        "annually",
        "only_after_changes",
        "only_after_major_changes",
        "as_needed",
        "no_formal_review",
        "never",
    ],
    "frequency_monitoring": [
        "continuously",
        "daily",
        "weekly",
        "monthly",
        "quarterly",
        "only_when_issues",
        "not_monitored",
        "never",
    ],
    "coverage": ["76_100", "51_75", "26_50", "0_25"],
    "implementation": [
        "fully_implemented",
        "partially_implemented",
        "planned",
        "not_implemented",
    ],
}

# Universal options that appear across many questions
UNIVERSAL_SLUGS = {
    "not sure": "not_sure",
    "unknown": "unknown",
    "not applicable": "not_applicable",
    "n/a": "not_applicable",
    "na": "not_applicable",
    "other": "other",
    "yes": "yes",
    "no": "no",
}


def slugify(text: str) -> str:
    """Convert text to a valid slug identifier"""
    # Lowercase and remove special characters
    slug = text.lower()
    # Replace spaces and special chars with underscores
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    # Remove leading/trailing underscores
    slug = slug.strip("_")
    # Collapse multiple underscores
    slug = re.sub(r"_+", "_", slug)
    return slug


def generate_slug_for_option(
    label: str, scale_type: str | None = None, index: int = 0
) -> str:
    """
    Generate a slug for an option based on its label and context

    Args:
        label: The option label text
        scale_type: The scale type if the question has one
        index: The 0-based index of the option

    Returns:
        A stable slug identifier
    """
    label_lower = label.lower().strip()

    # If question has a scale type, use scale slugs (highest priority)
    if scale_type and scale_type in SCALE_SLUGS:
        scale_options = SCALE_SLUGS[scale_type]
        if index < len(scale_options):
            return scale_options[index]

    # Check universal options (but only if not part of a scale)
    for pattern, slug in UNIVERSAL_SLUGS.items():
        if (
            label_lower == pattern
            or label_lower.startswith(pattern + " ")
            or label_lower.startswith(pattern + ",")
        ):
            return slug

    # Fallback: slugify the label
    return slugify(label)


def parse_questions_and_generate_mappings(md_file_path: str) -> dict:
    """
    Parse questions from markdown and generate slug mappings

    Returns:
        Dictionary mapping question_id to option mappings:
        {
            "1_1_1": {"1": "documented_approved_maintained", "2": "documented_but_stale", ...},
            ...
        }
    """
    with open(md_file_path, encoding="utf-8") as f:
        lines = f.readlines()

    mappings: dict[str, Any] = {}
    current_question = None
    current_question_id = None
    current_scale = None
    option_index = 0

    for _i, line in enumerate(lines):
        line_stripped = line.strip()

        # Detect question ID
        if line_stripped.startswith("#### Question"):
            if current_question and current_question["options"]:
                question_mapping = {}
                for opt in current_question["options"]:
                    question_mapping[opt["num"]] = opt["slug"]
                mappings[current_question_id] = question_mapping

            match = re.match(r"#### Question (.+)", line_stripped)
            if match:
                current_question_id = match.group(1).replace(".", "_")
                current_question = {"id": current_question_id, "options": []}
                current_scale = None
                option_index = 0

        # Detect scale type
        if current_question and line_stripped.startswith("**Scale:**"):
            current_scale = line_stripped.replace("**Scale:**", "").strip()

        # Detect options
        if current_question and line_stripped.startswith("**Option"):
            # Match numeric format: **Option 1:** or **Option 1:**
            option_match = re.match(r"\*\*Option (\d+):\s*(.+?)\*\*", line_stripped)
            if not option_match:
                option_match = re.match(r"\*\*Option (\d+):\*\*\s*(.+)", line_stripped)

            if option_match:
                option_num = option_match.group(1)
                option_label = option_match.group(2)

                # Generate slug for this option
                slug = generate_slug_for_option(
                    option_label, current_scale, option_index
                )

                # Ensure uniqueness within this question
                existing_slugs = [opt["slug"] for opt in current_question["options"]]
                if slug in existing_slugs:
                    # Append index to make unique
                    slug = f"{slug}_{option_index + 1}"

                current_question["options"].append(
                    {
                        "num": option_num,
                        "label": option_label,
                        "slug": slug,
                    }
                )
                option_index += 1

    # Save last question
    if current_question and current_question["options"]:
        question_mapping = {}
        for opt in current_question["options"]:
            question_mapping[opt["num"]] = opt["slug"]
        mappings[current_question_id] = question_mapping

    return mappings


def main() -> None:
    # Path to questions markdown file
    md_file = Path(__file__).parent.parent / "data" / "security_assessment_questions.md"

    print("Generating slug mappings for all questions...")
    print(f"Reading from: {md_file}")

    # Generate mappings
    mappings = parse_questions_and_generate_mappings(str(md_file))

    print(f"\nGenerated mappings for {len(mappings)} questions")

    # Output JSON file
    json_output = Path(__file__).parent / "slug_mappings.json"
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=2, sort_keys=True)
    print(f"Saved JSON mappings to: {json_output}")

    # Output CSV for human review
    csv_output = Path(__file__).parent / "slug_mappings.csv"
    with open(csv_output, "w", encoding="utf-8") as f:
        f.write("question_id,option_num,option_slug\n")
        for question_id in sorted(mappings.keys()):
            for option_num in sorted(mappings[question_id].keys(), key=int):
                slug = mappings[question_id][option_num]
                f.write(f"{question_id},{option_num},{slug}\n")
    print(f"Saved CSV for review to: {csv_output}")

    # Print some statistics
    total_options = sum(len(opts) for opts in mappings.values())
    print("\nStatistics:")
    print(f"  Total questions: {len(mappings)}")
    print(f"  Total options: {total_options}")
    print(f"  Average options per question: {total_options / len(mappings):.1f}")

    # Print sample mappings
    print("\nSample mappings (first 5 questions):")
    for question_id in sorted(mappings.keys())[:5]:
        print(f"  {question_id}: {mappings[question_id]}")


if __name__ == "__main__":
    main()
