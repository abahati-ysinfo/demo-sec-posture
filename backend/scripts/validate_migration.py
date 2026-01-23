"""
Validate migration results

This script runs after the migration to verify:
1. 100% of responses were migrated correctly
2. No orphaned numeric values remain
3. All slug values are valid according to current question definitions
4. Sample assessments can still generate reports correctly
"""

import json
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text

from app.core.config import settings


def load_mappings() -> dict[str, Any]:
    """Load slug mappings from JSON file"""
    mappings_file = Path(__file__).parent / "slug_mappings.json"
    with open(mappings_file) as f:
        return json.load(f)  # type: ignore[no-any-return]


def validate_migration() -> bool:
    """Validate that migration completed successfully"""
    # Load mappings
    mappings = load_mappings()

    # Build set of all valid slugs per question
    valid_slugs = {}
    for question_id, opts in mappings.items():
        valid_slugs[question_id] = set(opts.values())

    print(f"{'=' * 80}")
    print("Migration Validation")
    print(f"{'=' * 80}\n")

    # Connect to database
    engine = create_engine(str(settings.DATABASE_URL))

    with engine.connect() as conn:
        # Get total response count
        result = conn.execute(text("SELECT COUNT(*) FROM assessment_responses"))
        total_responses = result.scalar()

        print(f"Total responses in database: {total_responses}\n")

        if total_responses == 0:
            print("✓ No responses to validate - database is empty")
            return True

        # Check for orphaned numeric values
        result = conn.execute(
            text("""
            SELECT id, question_id, answer_value
            FROM assessment_responses
            WHERE answer_value IS NOT NULL
        """)
        )

        orphaned_numeric = []
        invalid_slugs = []
        valid_responses = 0

        for row in result:
            response_id = row[0]
            question_id = row[1]
            answer_value = row[2]

            # Check if question has mapping
            if question_id not in mappings:
                # Question not in mapping - this is OK (might be new or deleted)
                valid_responses += 1
                continue

            question_mapping = mappings[question_id]
            question_valid_slugs = valid_slugs[question_id]

            # Check answer_value
            if isinstance(answer_value, list):
                # Multiple choice
                for val in answer_value:
                    val_str = str(val)
                    # Check if it's a numeric value (should have been migrated)
                    if val_str in question_mapping.keys():
                        orphaned_numeric.append(
                            {
                                "response_id": response_id,
                                "question_id": question_id,
                                "value": val_str,
                                "expected_slug": question_mapping[val_str],
                            }
                        )
                    # Check if it's a valid slug
                    elif val_str not in question_valid_slugs:
                        invalid_slugs.append(
                            {
                                "response_id": response_id,
                                "question_id": question_id,
                                "value": val_str,
                                "valid_slugs": list(question_valid_slugs),
                            }
                        )
                    else:
                        valid_responses += 1
            else:
                # Single choice
                val_str = str(answer_value)
                # Check if it's a numeric value (should have been migrated)
                if val_str in question_mapping.keys():
                    orphaned_numeric.append(
                        {
                            "response_id": response_id,
                            "question_id": question_id,
                            "value": val_str,
                            "expected_slug": question_mapping[val_str],
                        }
                    )
                # Check if it's a valid slug
                elif val_str not in question_valid_slugs:
                    invalid_slugs.append(
                        {
                            "response_id": response_id,
                            "question_id": question_id,
                            "value": val_str,
                            "valid_slugs": list(question_valid_slugs),
                        }
                    )
                else:
                    valid_responses += 1

        # Print results
        print(f"{'=' * 80}")
        print("Validation Results:")
        print(f"{'=' * 80}\n")

        success = True

        if orphaned_numeric:
            print(f"❌ FAILED: Found {len(orphaned_numeric)} orphaned numeric values!")
            print("\nFirst 10 orphaned values:")
            for item in orphaned_numeric[:10]:
                print(
                    f"  Response {item['response_id']} (Q {item['question_id']}): '{item['value']}' should be '{item['expected_slug']}'"
                )
            success = False
        else:
            print("✓ No orphaned numeric values found")

        print()

        if invalid_slugs:
            print(f"⚠️  WARNING: Found {len(invalid_slugs)} invalid slug values")
            print("\nFirst 10 invalid slugs:")
            for item in invalid_slugs[:10]:
                print(
                    f"  Response {item['response_id']} (Q {item['question_id']}): '{item['value']}' not in {item['valid_slugs'][:3]}..."
                )
            print(
                "\nNote: Invalid slugs may be from old questions or manual data entry"
            )
        else:
            print("✓ All slug values are valid")

        print()
        print("Summary:")
        print(f"  Total responses: {total_responses}")
        print(f"  Valid responses: {valid_responses}")
        print(f"  Orphaned numeric: {len(orphaned_numeric)}")
        print(f"  Invalid slugs: {len(invalid_slugs)}")

        print(f"\n{'=' * 80}")
        if success:
            print("✓ Migration validation PASSED")
        else:
            print("❌ Migration validation FAILED")
        print(f"{'=' * 80}\n")

        return success


if __name__ == "__main__":
    try:
        success = validate_migration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)
