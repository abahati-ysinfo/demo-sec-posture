#!/usr/bin/env python3
"""
Questionnaire Linter - Detects placeholder options and content mismatches

This script scans the security assessment questionnaire markdown file to detect:
1. Placeholder options (e.g., "Option 1: Option 1", "Type A/B/C")
2. Generic descriptions (e.g., "First option", "Second option")
3. Content mismatches (e.g., SAST/DAST in non-Application Security sections)

Exit codes:
- 0: No issues found
- 1: Issues detected
"""

import re
import sys
from pathlib import Path
from typing import Any


class QuestionnaireIssue:
    """Represents an issue found in the questionnaire"""

    def __init__(
        self, line_num: int, issue_type: str, description: str, context: str = ""
    ):
        self.line_num = line_num
        self.issue_type = issue_type
        self.description = description
        self.context = context

    def __str__(self) -> str:
        return f"Line {self.line_num}: [{self.issue_type}] {self.description}\n  Context: {self.context}"


def load_questionnaire(file_path: Path) -> list[str]:
    """Load questionnaire file into memory"""
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Questionnaire file not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to read questionnaire: {e}", file=sys.stderr)
        sys.exit(1)


def detect_placeholder_options(lines: list[str]) -> list[QuestionnaireIssue]:
    """Detect placeholder option patterns"""
    issues = []

    option_pattern = re.compile(r"\*\*Option\s+(\d+):\s+Option\s+\1\*\*")

    type_pattern = re.compile(r"\*\*Option\s+\d+:\s+Type\s+[A-Z]\*\*")

    generic_desc_patterns = [
        re.compile(
            r"\*Basic Description:\*\s+(First|Second|Third|Fourth|Fifth)\s+option"
        ),
        re.compile(r"\*Basic Description:\*\s+Primary\s+implementation\s+type"),
        re.compile(r"\*Basic Description:\*\s+Secondary\s+implementation\s+type"),
        re.compile(r"\*Basic Description:\*\s+Alternative\s+implementation\s+type"),
    ]

    for i, line in enumerate(lines, start=1):
        if option_pattern.search(line):
            issues.append(
                QuestionnaireIssue(
                    i,
                    "PLACEHOLDER_OPTION",
                    "Placeholder option label detected",
                    line.strip(),
                )
            )

        if type_pattern.search(line):
            issues.append(
                QuestionnaireIssue(
                    i,
                    "PLACEHOLDER_OPTION",
                    "Generic type placeholder detected",
                    line.strip(),
                )
            )

        for pattern in generic_desc_patterns:
            if pattern.search(line):
                issues.append(
                    QuestionnaireIssue(
                        i,
                        "GENERIC_DESCRIPTION",
                        "Generic placeholder description detected",
                        line.strip(),
                    )
                )

    return issues


def detect_content_mismatches(lines: list[str]) -> list[QuestionnaireIssue]:
    """Detect content mismatches (e.g., SAST in wrong sections)"""
    issues = []
    current_section = ""

    section_pattern = re.compile(r"^##\s+Section\s+\d+:\s+(.+)$")
    sast_dast_pattern = re.compile(
        r"(SAST|DAST|static\s+analysis|dynamic\s+analysis)", re.IGNORECASE
    )

    for i, line in enumerate(lines, start=1):
        section_match = section_pattern.match(line)
        if section_match:
            current_section = section_match.group(1).strip()
            continue

        if sast_dast_pattern.search(line):
            if (
                "Application Security" not in current_section
                and "DevSecOps" not in current_section
            ):
                if "**Option" in line or "*Basic Description:*" in line:
                    issues.append(
                        QuestionnaireIssue(
                            i,
                            "CONTENT_MISMATCH",
                            f"SAST/DAST reference found in '{current_section}' section (should only be in Application Security)",
                            line.strip(),
                        )
                    )

    return issues


def detect_todo_placeholders(lines: list[str]) -> list[QuestionnaireIssue]:
    """Detect TODO, TBD, and other placeholder markers"""
    issues = []

    placeholder_markers = [
        re.compile(r"\bTODO\b", re.IGNORECASE),
        re.compile(r"\bTBD\b", re.IGNORECASE),
        re.compile(r"\bFIXME\b", re.IGNORECASE),
        re.compile(r"\bXXX\b"),
        re.compile(r"\bplaceholder\b", re.IGNORECASE),
        re.compile(r"\bexample\b.*\boption\b", re.IGNORECASE),
    ]

    for i, line in enumerate(lines, start=1):
        for pattern in placeholder_markers:
            if pattern.search(line):
                issues.append(
                    QuestionnaireIssue(
                        i,
                        "TODO_PLACEHOLDER",
                        "TODO/TBD/placeholder marker detected",
                        line.strip(),
                    )
                )
                break  # Only report once per line

    return issues


def main() -> None:
    """Main linter function"""
    script_dir = Path(__file__).parent
    questionnaire_path = script_dir.parent / "data" / "security_assessment_questions.md"

    if not questionnaire_path.exists():
        print(
            f"ERROR: Questionnaire file not found: {questionnaire_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Linting questionnaire: {questionnaire_path}")
    print("-" * 80)

    lines = load_questionnaire(questionnaire_path)

    all_issues = []
    all_issues.extend(detect_placeholder_options(lines))
    all_issues.extend(detect_content_mismatches(lines))
    all_issues.extend(detect_todo_placeholders(lines))

    all_issues.sort(key=lambda x: x.line_num)

    if not all_issues:
        print("✅ No issues found! Questionnaire is clean.")
        sys.exit(0)
    else:
        print(f"❌ Found {len(all_issues)} issue(s):\n")

        by_type: dict[str, Any] = {}
        for issue in all_issues:
            if issue.issue_type not in by_type:
                by_type[issue.issue_type] = []
            by_type[issue.issue_type].append(issue)

        for issue_type, issues in by_type.items():
            print(f"\n{issue_type}: {len(issues)} issue(s)")
            print("-" * 80)
            for issue in issues:
                print(f"  {issue}")

        print(f"\n{'=' * 80}")
        print(f"Total issues: {len(all_issues)}")
        print(f"{'=' * 80}")

        sys.exit(1)


if __name__ == "__main__":
    main()
