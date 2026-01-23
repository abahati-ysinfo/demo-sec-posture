"""
Update security_assessment_questions.md to use slug-format options

This script:
1. Reads the slug mappings from slug_mappings.json
2. Updates all option lines from **Option 1:** to **Option slug:**
3. Preserves all other content (explanations, descriptions, etc.)
4. Creates a backup of the original file
5. Validates the updated file has the same number of questions
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path


def update_markdown_with_slugs(md_file_path: str, mappings_file_path: str) -> None:
    """
    Update markdown file to use slug-format options

    Args:
        md_file_path: Path to security_assessment_questions.md
        mappings_file_path: Path to slug_mappings.json
    """
    # Load slug mappings
    with open(mappings_file_path, encoding="utf-8") as f:
        mappings = json.load(f)

    print(f"Loaded mappings for {len(mappings)} questions")

    # Create backup
    backup_path = f"{md_file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(md_file_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read original file
    with open(md_file_path, encoding="utf-8") as f:
        lines = f.readlines()

    # Process lines
    updated_lines = []
    current_question_id = None
    questions_updated = 0
    options_updated = 0

    for _i, line in enumerate(lines):
        line_stripped = line.strip()

        # Detect question ID
        if line_stripped.startswith("#### Question"):
            match = re.match(r"#### Question (.+)", line_stripped)
            if match:
                current_question_id = match.group(1).replace(".", "_")
                if current_question_id in mappings:
                    questions_updated += 1

        # Update option lines
        if current_question_id and line_stripped.startswith("**Option"):
            # Match numeric format: **Option 1:** Label** or **Option 1:** followed by text on next line
            option_match = re.match(r"^(\*\*Option )(\d+)(:.*)$", line_stripped)

            if option_match and current_question_id in mappings:
                prefix = option_match.group(1)
                option_num = option_match.group(2)
                suffix = option_match.group(3)

                # Get slug for this option
                if option_num in mappings[current_question_id]:
                    slug = mappings[current_question_id][option_num]

                    # Replace numeric with slug, preserving indentation
                    indent = line[: len(line) - len(line.lstrip())]
                    updated_line = f"{indent}{prefix}{slug}{suffix}\n"
                    updated_lines.append(updated_line)
                    options_updated += 1
                    continue

        # Keep line unchanged
        updated_lines.append(line)

    # Write updated file
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print("\nUpdate complete!")
    print(f"  Questions updated: {questions_updated}")
    print(f"  Options updated: {options_updated}")
    print(f"  Original file backed up to: {backup_path}")

    # Validate
    print("\nValidating updated file...")
    with open(md_file_path, encoding="utf-8") as f:
        updated_content = f.read()

    # Count questions
    question_count = updated_content.count("#### Question")
    print(f"  Questions in updated file: {question_count}")

    # Check for remaining numeric options
    numeric_options = re.findall(r"\*\*Option \d+:", updated_content)
    if numeric_options:
        print(
            f"  ⚠️  WARNING: Found {len(numeric_options)} numeric options still remaining!"
        )
        print(f"     First few: {numeric_options[:5]}")
    else:
        print("  ✓ No numeric options remaining - all converted to slugs!")

    # Check for slug options
    slug_options = re.findall(r"\*\*Option [a-z_]+:", updated_content)
    print(f"  Slug-format options found: {len(slug_options)}")


def main() -> None:
    # Paths
    script_dir = Path(__file__).parent
    md_file = script_dir.parent / "data" / "security_assessment_questions.md"
    mappings_file = script_dir / "slug_mappings.json"

    print("Updating security_assessment_questions.md with slug-format options...")
    print(f"Markdown file: {md_file}")
    print(f"Mappings file: {mappings_file}")
    print()

    # Check files exist
    if not md_file.exists():
        print(f"ERROR: Markdown file not found: {md_file}")
        return

    if not mappings_file.exists():
        print(f"ERROR: Mappings file not found: {mappings_file}")
        print("Please run generate_slug_mappings.py first!")
        return

    # Update markdown
    update_markdown_with_slugs(str(md_file), str(mappings_file))


if __name__ == "__main__":
    main()
