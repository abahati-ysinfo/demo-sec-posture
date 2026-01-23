"""
Dry-run migration preview script

This script shows what would be migrated without changing the database.
It connects to the database and shows:
- How many responses would be affected
- Sample transformations (Question X: '1' → 'quarterly')
- Questions with no responses
- Responses that would be skipped (already slugs)
"""

import json
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text

from app.core.config import settings


def load_mappings() -> Any:
    """Load slug mappings from JSON file"""
    mappings_file = Path(__file__).parent / "slug_mappings.json"
    with open(mappings_file) as f:
        return json.load(f)


def preview_migration() -> None:
    """Preview what the migration would do"""
    # Load mappings
    mappings = load_mappings()
    print(f"Loaded mappings for {len(mappings)} questions\n")

    # Connect to database
    engine = create_engine(str(settings.DATABASE_URL))

    with engine.connect() as conn:
        # Get total response count
        result = conn.execute(text("SELECT COUNT(*) FROM assessment_responses"))
        total_responses = result.scalar()

        print(f"{'=' * 80}")
        print("DRY RUN: Migration Preview")
        print(f"{'=' * 80}\n")
        print(f"Total responses in database: {total_responses}\n")

        if total_responses == 0:
            print("No responses to migrate - database is empty")
            return

        # Analyze responses by question
        result = conn.execute(
            text("""
            SELECT question_id, answer_value, COUNT(*) as count
            FROM assessment_responses
            WHERE answer_value IS NOT NULL
            GROUP BY question_id, answer_value
            ORDER BY question_id, answer_value
        """)
        )

        responses_to_migrate = 0
        responses_to_skip = 0
        questions_with_data = set()

        print(f"{'=' * 80}")
        print("Sample Transformations (first 20):")
        print(f"{'=' * 80}\n")

        sample_count = 0
        for row in result:
            question_id = row[0]
            answer_value = row[1]
            count = row[2]

            questions_with_data.add(question_id)

            # Check if this question has a mapping
            if question_id not in mappings:
                responses_to_skip += count
                if sample_count < 20:
                    print(
                        f"  Question {question_id}: SKIP (no mapping) - {count} response(s)"
                    )
                    sample_count += 1
                continue

            question_mapping = mappings[question_id]

            # Check if answer_value needs migration
            if isinstance(answer_value, list):
                # Multiple choice
                needs_migration = any(
                    str(val) in question_mapping for val in answer_value
                )
                if needs_migration:
                    new_values = []
                    for val in answer_value:
                        val_str = str(val)
                        if val_str in question_mapping:
                            new_values.append(question_mapping[val_str])
                        else:
                            new_values.append(val)

                    responses_to_migrate += count
                    if sample_count < 20:
                        print(
                            f"  Question {question_id}: {answer_value} → {new_values} - {count} response(s)"
                        )
                        sample_count += 1
                else:
                    responses_to_skip += count
                    if sample_count < 20:
                        print(
                            f"  Question {question_id}: SKIP (already slugs) - {count} response(s)"
                        )
                        sample_count += 1
            else:
                # Single choice
                val_str = str(answer_value)
                if val_str in question_mapping:
                    new_value = question_mapping[val_str]
                    responses_to_migrate += count
                    if sample_count < 20:
                        print(
                            f"  Question {question_id}: '{answer_value}' → '{new_value}' - {count} response(s)"
                        )
                        sample_count += 1
                else:
                    responses_to_skip += count
                    if sample_count < 20:
                        print(
                            f"  Question {question_id}: SKIP (already slug) - {count} response(s)"
                        )
                        sample_count += 1

        print(f"\n{'=' * 80}")
        print("Summary:")
        print(f"{'=' * 80}\n")
        print(f"  Total responses: {total_responses}")
        print(f"  Responses to migrate: {responses_to_migrate}")
        print(f"  Responses to skip: {responses_to_skip}")
        print(f"  Questions with data: {len(questions_with_data)}")
        print(f"  Questions in mapping: {len(mappings)}")
        print(f"  Questions without data: {len(mappings) - len(questions_with_data)}")
        print(f"\n{'=' * 80}")
        print("This was a DRY RUN - no changes were made to the database")
        print(f"{'=' * 80}\n")


if __name__ == "__main__":
    try:
        preview_migration()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
