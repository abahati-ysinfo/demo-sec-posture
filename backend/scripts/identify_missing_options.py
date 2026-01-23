#!/usr/bin/env python3
"""
Identify questions that need "Not sure" or "Not applicable" options
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.question_parser import parse_assessment_questions


def identify_missing_options() -> None:
    """Scan questions for missing options"""

    md_path = Path(__file__).parent.parent / "data" / "security_assessment_questions.md"
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    structure = parse_assessment_questions(content)

    technical_sections = {
        "4": "Identity & Access Management (IAM)",
        "8": "Application Security & SDLC",
        "9": "Cloud & Container Security",
        "10": "DevSecOps & CI/CD Security",
        "15": "Security Monitoring & Detection",
        "16": "Vulnerability Management",
    }

    domain_specific_sections = {
        "18": "OT/ICS & IoT Security",
        "19": "AI/ML Security",
    }

    needs_not_sure = []
    needs_not_applicable = []

    for section in structure.sections:
        section_num = section.id.split("_")[1] if "_" in section.id else section.id

        for question in section.questions:
            if question.type not in ["multiple_choice", "multiple_select"]:
                continue

            option_labels = [opt.label.lower() for opt in question.options]

            if section_num in technical_sections:
                has_not_sure = any(
                    "not sure" in label
                    or "unknown" in label
                    or "don't know" in label
                    or "unclear" in label
                    for label in option_labels
                )
                if not has_not_sure:
                    needs_not_sure.append(
                        {
                            "id": question.id,
                            "section": section.title,
                            "text": question.text[:80] + "..."
                            if len(question.text) > 80
                            else question.text,
                            "type": question.type,
                            "options_count": len(question.options),
                        }
                    )

            if section_num in domain_specific_sections:
                has_not_applicable = any(
                    "not applicable" in label
                    or "n/a" in label
                    or "does not apply" in label
                    for label in option_labels
                )
                if not has_not_applicable:
                    needs_not_applicable.append(
                        {
                            "id": question.id,
                            "section": section.title,
                            "text": question.text[:80] + "..."
                            if len(question.text) > 80
                            else question.text,
                            "type": question.type,
                            "options_count": len(question.options),
                        }
                    )

    print("=" * 80)
    print("PHASE 4: SYSTEMATIC IMPROVEMENTS - MISSING OPTIONS ANALYSIS")
    print("=" * 80)
    print()

    print("📊 SUMMARY:")
    print(f"  - Questions needing 'Not sure': {len(needs_not_sure)}")
    print(f"  - Questions needing 'Not applicable': {len(needs_not_applicable)}")
    print()

    if needs_not_sure:
        print("=" * 80)
        print("QUESTIONS NEEDING 'NOT SURE' OPTION (Technical Sections)")
        print("=" * 80)
        print()
        for i, q in enumerate(needs_not_sure, 1):
            print(
                f"{i}. Question {q['id']} ({q['type']}, {q['options_count']} options)"
            )
            print(f"   Section: {q['section']}")
            print(f"   Text: {q['text']}")
            print()

    if needs_not_applicable:
        print("=" * 80)
        print("QUESTIONS NEEDING 'NOT APPLICABLE' OPTION (Domain-Specific Sections)")
        print("=" * 80)
        print()
        for i, q in enumerate(needs_not_applicable, 1):
            print(
                f"{i}. Question {q['id']} ({q['type']}, {q['options_count']} options)"
            )
            print(f"   Section: {q['section']}")
            print(f"   Text: {q['text']}")
            print()

    output_path = Path(__file__).parent / "missing_options_report.txt"
    with open(output_path, "w") as f:
        f.write("PHASE 4: SYSTEMATIC IMPROVEMENTS - MISSING OPTIONS ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Questions needing 'Not sure': {len(needs_not_sure)}\n")
        f.write(f"Questions needing 'Not applicable': {len(needs_not_applicable)}\n\n")

        if needs_not_sure:
            f.write("QUESTIONS NEEDING 'NOT SURE' OPTION:\n")
            f.write("-" * 80 + "\n")
            for q in needs_not_sure:
                f.write(f"Question {q['id']}: {q['text']}\n")
            f.write("\n")

        if needs_not_applicable:
            f.write("QUESTIONS NEEDING 'NOT APPLICABLE' OPTION:\n")
            f.write("-" * 80 + "\n")
            for q in needs_not_applicable:
                f.write(f"Question {q['id']}: {q['text']}\n")
            f.write("\n")

    print(f"📝 Report saved to: {output_path}")
    print()

    return needs_not_sure, needs_not_applicable  # type: ignore[return-value]


if __name__ == "__main__":
    identify_missing_options()
