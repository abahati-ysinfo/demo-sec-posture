#!/usr/bin/env python3
"""
Identify frequency scale inconsistencies across questions
"""

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.question_parser import parse_assessment_questions


def identify_frequency_inconsistencies() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]]
]:
    """Scan questions for frequency scale inconsistencies"""

    md_path = Path(__file__).parent.parent / "data" / "security_assessment_questions.md"
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    structure = parse_assessment_questions(content)

    review_keywords = ["review", "update", "assess", "evaluate", "audit"]
    monitoring_keywords = ["monitor", "scan", "check", "test", "detect"]

    frequency_questions = []

    for section in structure.sections:
        for question in section.questions:
            question_lower = question.text.lower()

            is_frequency = any(
                keyword in question_lower
                for keyword in ["how often", "how frequently", "frequency", "cadence"]
            )

            if is_frequency:
                question_type = "unknown"
                if any(kw in question_lower for kw in review_keywords):
                    question_type = "review"
                elif any(kw in question_lower for kw in monitoring_keywords):
                    question_type = "monitoring"

                options = [opt.label for opt in question.options]

                frequency_questions.append(
                    {
                        "id": question.id,
                        "section": section.title,
                        "text": question.text[:80] + "..."
                        if len(question.text) > 80
                        else question.text,
                        "type": question_type,
                        "scale": question.scale if hasattr(question, "scale") else None,
                        "options": options,
                        "options_count": len(options),
                    }
                )

    option_patterns = defaultdict(list)
    for q in frequency_questions:
        pattern = tuple(sorted([opt.lower() for opt in q["options"]]))  # type: ignore[union-attr]
        option_patterns[pattern].append(q)

    print("=" * 80)
    print("PHASE 4: SYSTEMATIC IMPROVEMENTS - FREQUENCY SCALE ANALYSIS")
    print("=" * 80)
    print()

    print("📊 SUMMARY:")
    print(f"  - Total frequency questions found: {len(frequency_questions)}")
    print(
        f"  - Review-type questions: {sum(1 for q in frequency_questions if q['type'] == 'review')}"
    )
    print(
        f"  - Monitoring-type questions: {sum(1 for q in frequency_questions if q['type'] == 'monitoring')}"
    )
    print(
        f"  - Unknown type: {sum(1 for q in frequency_questions if q['type'] == 'unknown')}"
    )
    print(f"  - Unique option patterns: {len(option_patterns)}")
    print()

    print("=" * 80)
    print("FREQUENCY QUESTIONS BY TYPE")
    print("=" * 80)
    print()

    review_questions = [q for q in frequency_questions if q["type"] == "review"]
    if review_questions:
        print("REVIEW-TYPE QUESTIONS (should use frequency_review scale):")
        print("-" * 80)
        for i, q in enumerate(review_questions, 1):
            print(f"{i}. Question {q['id']} (Scale: {q['scale'] or 'None'})")
            print(f"   Section: {q['section']}")
            print(f"   Text: {q['text']}")
            print(f"   Options: {', '.join(q['options'])}")  # type: ignore[arg-type]
            print()

    monitoring_questions = [q for q in frequency_questions if q["type"] == "monitoring"]
    if monitoring_questions:
        print("=" * 80)
        print("MONITORING-TYPE QUESTIONS (should use frequency_monitoring scale):")
        print("-" * 80)
        for i, q in enumerate(monitoring_questions, 1):
            print(f"{i}. Question {q['id']} (Scale: {q['scale'] or 'None'})")
            print(f"   Section: {q['section']}")
            print(f"   Text: {q['text']}")
            print(f"   Options: {', '.join(q['options'])}")  # type: ignore[arg-type]
            print()

    print("=" * 80)
    print("UNIQUE OPTION PATTERNS (showing inconsistencies)")
    print("=" * 80)
    print()

    for i, (pattern, questions) in enumerate(
        sorted(option_patterns.items(), key=lambda x: -len(x[1])), 1
    ):
        if len(questions) > 1:
            print(f"Pattern {i} (used by {len(questions)} questions):")
            print(f"  Options: {', '.join(sorted(pattern))}")
            print("  Questions:")
            for q in questions[:5]:  # Show first 5
                print(f"    - {q['id']}: {q['text']}")
            if len(questions) > 5:
                print(f"    ... and {len(questions) - 5} more")
            print()

    needs_normalization = []

    canonical_review = {
        "quarterly",
        "annually",
        "only after major changes/incidents",
        "no formal review schedule",
    }
    canonical_monitoring = {
        "continuously",
        "daily",
        "weekly",
        "monthly",
        "quarterly",
        "only when issues occur",
        "not monitored",
    }

    for q in frequency_questions:
        options_lower = {opt.lower() for opt in q["options"]}  # type: ignore[union-attr]

        if q["type"] == "review":
            if q["scale"] != "frequency_review":
                needs_normalization.append(
                    {
                        **q,
                        "reason": f"Missing frequency_review scale (current: {q['scale'] or 'None'})",
                    }
                )
            elif not options_lower.issubset(canonical_review):
                needs_normalization.append(
                    {
                        **q,
                        "reason": "Options don't match canonical frequency_review scale",
                    }
                )
        elif q["type"] == "monitoring":
            if q["scale"] != "frequency_monitoring":
                needs_normalization.append(
                    {
                        **q,
                        "reason": f"Missing frequency_monitoring scale (current: {q['scale'] or 'None'})",
                    }
                )
            elif not options_lower.issubset(canonical_monitoring):
                needs_normalization.append(
                    {
                        **q,
                        "reason": "Options don't match canonical frequency_monitoring scale",
                    }
                )

    if needs_normalization:
        print("=" * 80)
        print("QUESTIONS NEEDING NORMALIZATION")
        print("=" * 80)
        print()
        for i, q in enumerate(needs_normalization, 1):
            print(f"{i}. Question {q['id']}")
            print(f"   Section: {q['section']}")
            print(f"   Text: {q['text']}")
            print(f"   Reason: {q['reason']}")
            print(f"   Current options: {', '.join(q['options'])}")  # type: ignore[arg-type]
            print()

    output_path = Path(__file__).parent / "frequency_inconsistencies_report.txt"
    with open(output_path, "w") as f:
        f.write("PHASE 4: SYSTEMATIC IMPROVEMENTS - FREQUENCY SCALE ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total frequency questions: {len(frequency_questions)}\n")
        f.write(f"Questions needing normalization: {len(needs_normalization)}\n\n")

        if needs_normalization:
            f.write("QUESTIONS NEEDING NORMALIZATION:\n")
            f.write("-" * 80 + "\n")
            for q in needs_normalization:
                f.write(f"Question {q['id']}: {q['text']}\n")
                f.write(f"  Reason: {q['reason']}\n")
                f.write(f"  Current options: {', '.join(q['options'])}\n\n")  # type: ignore[arg-type]  # noqa

    print(f"📝 Report saved to: {output_path}")
    print()

    return frequency_questions, needs_normalization


if __name__ == "__main__":
    identify_frequency_inconsistencies()
