#!/usr/bin/env python3
"""
Apply Phase 4 systematic improvements to questions file
"""

import re
import sys
from pathlib import Path

FREQUENCY_REVIEW_QUESTIONS = [
    "2_1_1",
    "2_1_7",
    "2_3_5",
    "3_1_6",
    "5_2_2",
    "6_1_5",
    "6_3_4",
    "10_1_2",
    "11_1_2",
    "12_1_5",
    "14_1_6",
    "17_2_2",
]

FREQUENCY_MONITORING_QUESTIONS = ["16_1_2"]

NOT_SURE_QUESTIONS = [
    "1_4_9",
    "4_1_1",
    "4_1_2",
    "4_1_4",
    "4_1_6",
    "4_1_8",
    "4_2_1",
    "4_2_3",
    "4_2_5",
    "4_3_2",
    "4_3_3",
    "4_3_4",
    "4_3_6",
    "4_4_2",
    "4_4_3",
    "7_4_5",
    "8_1_2",
    "8_1_3",
    "8_1_6",
    "8_2_6",
    "8_3_1",
    "8_3_4",
    "8_4_1",
    "8_4_2",
    "8_4_3",
    "8_4_4",
    "8_4_5",
    "8_4_6",
    "8_4_7",
    "9_1_1",
    "9_1_3",
    "9_1_4",
    "9_1_5",
    "9_1_7",
    "9_2_1",
    "9_2_3",
    "9_2_4",
    "9_2_5",
    "9_3_2",
    "9_3_3",
    "9_3_4",
    "9_3_6",
    "10_1_2",
    "10_1_4",
    "10_1_5",
    "10_1_6",
    "10_2_1",
    "10_2_2",
    "10_2_4",
    "10_2_6",
    "10_3_2",
    "10_3_5",
    "14_3_16",
    "15_1_2",
    "15_1_4",
    "15_1_5",
    "15_1_7",
    "15_2_2",
    "15_2_3",
    "15_2_4",
    "15_2_6",
    "15_3_2",
    "15_3_3",
    "15_3_4",
    "15_3_5",
    "16_1_2",
    "16_1_3",
    "16_1_5",
    "16_1_6",
    "16_2_2",
    "16_2_3",
    "16_2_4",
    "16_2_6",
    "16_3_2",
    "16_3_3",
    "16_3_4",
    "16_3_5",
    "16_3_6",
    "16_3_7",
]

NOT_APPLICABLE_QUESTIONS = [
    "17_3_7",
    "18_1_2",
    "18_1_4",
    "18_1_5",
    "18_2_2",
    "18_2_3",
    "18_2_4",
    "18_2_5",
    "19_1_3",
    "19_1_4",
    "19_1_5",
    "19_2_1",
    "19_2_3",
    "19_2_4",
]


def apply_phase4_updates() -> None:
    """Apply Phase 4 systematic improvements"""

    md_path = Path(__file__).parent.parent / "data" / "security_assessment_questions.md"

    print("Reading questions file...")
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    updated_lines = []
    current_question_id = None
    in_question = False
    scale_added = False
    last_option_num = 0
    question_type = None

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("#### Question "):
            match = re.match(r"#### Question (\d+\.\d+\.\d+)", line)
            if match:
                current_question_id = match.group(1).replace(".", "_")
                in_question = True
                scale_added = False
                last_option_num = 0
                question_type = None

        if in_question and line.startswith("**Type:**"):
            question_type = line.split("**Type:**")[1].strip()

        if (
            in_question
            and current_question_id
            and line.startswith("**Explanation:**")
            and not scale_added
        ):
            if current_question_id in FREQUENCY_REVIEW_QUESTIONS:
                updated_lines.append("")
                updated_lines.append("**Scale:** frequency_review")
                scale_added = True
                print(
                    f"  ✓ Added frequency_review scale to Question {current_question_id.replace('_', '.')}"
                )
            elif current_question_id in FREQUENCY_MONITORING_QUESTIONS:
                updated_lines.append("")
                updated_lines.append("**Scale:** frequency_monitoring")
                scale_added = True
                print(
                    f"  ✓ Added frequency_monitoring scale to Question {current_question_id.replace('_', '.')}"
                )

        if in_question and line.startswith("**Option "):
            match = re.match(r"\*\*Option (\d+):", line)
            if match:
                last_option_num = int(match.group(1))

        if in_question and current_question_id:
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            is_end_of_options = (
                next_line.strip() == ""
                and i + 2 < len(lines)
                and lines[i + 2].startswith("###")
            ) or (next_line.startswith("###"))

            if is_end_of_options and last_option_num > 0:
                if current_question_id in NOT_SURE_QUESTIONS and question_type in [
                    "multiple_choice",
                    "multiple_select",
                ]:
                    has_not_sure = False
                    for check_line in updated_lines[-20:]:  # Check last 20 lines
                        if (
                            "not sure" in check_line.lower()
                            or "unknown" in check_line.lower()
                        ):
                            has_not_sure = True
                            break

                    if not has_not_sure:
                        updated_lines.append("")
                        updated_lines.append(
                            f"**Option {last_option_num + 1}: Not sure**"
                        )
                        updated_lines.append("*Basic Description:* Unclear or unknown")
                        print(
                            f"  ✓ Added 'Not sure' option to Question {current_question_id.replace('_', '.')}"
                        )
                        last_option_num += 1

                if (
                    current_question_id in NOT_APPLICABLE_QUESTIONS
                    and question_type in ["multiple_choice", "multiple_select"]
                ):
                    has_not_applicable = False
                    for check_line in updated_lines[-20:]:  # Check last 20 lines
                        if (
                            "not applicable" in check_line.lower()
                            or "n/a" in check_line.lower()
                        ):
                            has_not_applicable = True
                            break

                    if not has_not_applicable:
                        updated_lines.append("")
                        updated_lines.append(
                            f"**Option {last_option_num + 1}: Not applicable**"
                        )
                        updated_lines.append(
                            "*Basic Description:* Does not apply to our organization"
                        )
                        print(
                            f"  ✓ Added 'Not applicable' option to Question {current_question_id.replace('_', '.')}"
                        )
                        last_option_num += 1

                if next_line.startswith("###"):
                    in_question = False
                    current_question_id = None

        updated_lines.append(line)
        i += 1

    print("\nWriting updated questions file...")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_lines))

    print("\n✅ Phase 4 systematic improvements applied successfully!")
    print(
        f"   - Added frequency scales to {len(FREQUENCY_REVIEW_QUESTIONS) + len(FREQUENCY_MONITORING_QUESTIONS)} questions"
    )
    print(f"   - Added 'Not sure' options to {len(NOT_SURE_QUESTIONS)} questions")
    print(
        f"   - Added 'Not applicable' options to {len(NOT_APPLICABLE_QUESTIONS)} questions"
    )


if __name__ == "__main__":
    try:
        apply_phase4_updates()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
