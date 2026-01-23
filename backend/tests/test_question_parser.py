from app.services.question_parser import (
    _parse_option_explanation,
    create_sample_assessment_structure,
    load_assessment_structure,
    parse_assessment_questions,
)


def test_load_assessment_structure() -> None:
    structure = load_assessment_structure()

    assert structure is not None
    assert hasattr(structure, "sections")
    assert hasattr(structure, "total_questions")
    assert structure.total_questions > 0
    assert len(structure.sections) > 0


def test_assessment_structure_has_required_fields() -> None:
    structure = load_assessment_structure()

    assert hasattr(structure, "sections")
    assert hasattr(structure, "total_questions")

    for section in structure.sections:
        assert hasattr(section, "id")
        assert hasattr(section, "title")
        assert hasattr(section, "questions")


def test_question_types_are_valid() -> None:
    structure = load_assessment_structure()

    valid_types = ["yes_no", "multiple_choice", "multiple_select", "text"]

    for section in structure.sections:
        for question in section.questions:
            assert question.type in valid_types


def test_total_questions_count() -> None:
    structure = load_assessment_structure()

    actual_count = sum(len(section.questions) for section in structure.sections)

    assert structure.total_questions == actual_count
    assert structure.total_questions > 0


def test_create_sample_assessment_structure() -> None:
    structure = create_sample_assessment_structure()

    assert structure is not None
    assert hasattr(structure, "sections")
    assert structure.total_questions > 0
    assert len(structure.sections) == 2


def test_parse_option_explanation_with_full_details() -> None:
    """Test parsing option explanation with all sections present"""
    lines = [
        "**📋 What This Option Means:**",
        "This is the definition of the option.",
        "",
        "**📊 Market Context & Benchmarks:**",
        "- **Industry Adoption Rate:** 75% of organizations",
        "- **Industry Benchmark:** Leading practice",
        "- **Compliance Frameworks:** ISO 27001, SOC 2",
        "",
        "**🎯 Recommendations & Next Steps:**",
        "This is the recommendation.",
        "",
        "**Option 2: Another option**",
    ]

    result = _parse_option_explanation(lines, 0)

    assert result is not None
    assert result["definition"] == "This is the definition of the option."
    assert "75% of organizations" in result["industry_adoption_rate"]
    assert "Leading practice" in result["industry_benchmark"]
    assert "ISO 27001, SOC 2" in result["compliance_frameworks"]
    assert result["recommendation"] == "This is the recommendation."


def test_parse_option_explanation_with_minimal_details() -> None:
    """Test parsing option explanation with only definition"""
    lines = [
        "**📋 What This Option Means:**",
        "Just a definition.",
        "",
        "**Option 2: Another option**",
    ]

    result = _parse_option_explanation(lines, 0)

    assert result is not None
    assert result["definition"] == "Just a definition."
    assert result["industry_adoption_rate"] is None
    assert result["recommendation"] is None


def test_parse_option_explanation_no_detailed_explanation() -> None:
    """Test parsing when no detailed explanation is present"""
    lines = [
        "*Basic Description: Simple description*",
        "",
        "**Option 2: Another option**",
    ]

    result = _parse_option_explanation(lines, 0)

    assert result is None


def test_parse_option_explanation_case_insensitive() -> None:
    """Test that parsing is case-insensitive for headings"""
    lines = [
        "**what this option means:**",
        "Definition text.",
        "",
        "**RECOMMENDATIONS & next steps:**",
        "Recommendation text.",
        "",
        "**Option 2: Another option**",
    ]

    result = _parse_option_explanation(lines, 0)

    assert result is not None
    assert result["definition"] == "Definition text."
    assert result["recommendation"] == "Recommendation text."


def test_parse_option_explanation_emoji_agnostic() -> None:
    """Test that parsing works without emojis"""
    lines = [
        "**What This Option Means:**",
        "Definition without emoji.",
        "",
        "**Market Context & Benchmarks:**",
        "- **Industry Adoption Rate:** 50%",
        "",
        "**Recommendations & Next Steps:**",
        "Recommendation without emoji.",
        "",
        "**Option 2: Another option**",
    ]

    result = _parse_option_explanation(lines, 0)

    assert result is not None
    assert result["definition"] == "Definition without emoji."
    assert "50%" in result["industry_adoption_rate"]
    assert result["recommendation"] == "Recommendation without emoji."


def test_loaded_structure_has_explanations() -> None:
    """Test that loaded structure includes detailed explanations for some options"""
    structure = load_assessment_structure()

    options_with_explanations = 0
    total_options = 0

    for section in structure.sections:
        for question in section.questions:
            for option in question.options:
                total_options += 1
                if option.detailed_explanation is not None:
                    options_with_explanations += 1

    assert total_options > 0
    assert options_with_explanations >= 0


def test_parse_slug_format_options() -> None:
    """Test parsing options with slug format (Phase 3a)"""
    md_content = """
## Section 1: Test Section

### 1.1 Test Subsection

#### Question 1.1.1

**Question:** How often do you review your security strategy?

**Type:** multiple_choice

**Weight:** 3

**Scale:** frequency_review

**Explanation:** Regular reviews are important.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option never:** Never
"""

    structure = parse_assessment_questions(md_content)

    assert len(structure.sections) == 1
    assert len(structure.sections[0].questions) == 1

    question = structure.sections[0].questions[0]
    assert len(question.options) == 3
    assert question.options[0].value == "quarterly"
    assert question.options[0].label == "Quarterly"
    assert question.options[1].value == "annually"
    assert question.options[1].label == "Annually"
    assert question.options[2].value == "never"
    assert question.options[2].label == "Never"


def test_parse_numeric_format_options() -> None:
    """Test parsing options with numeric format (backward compatibility)"""
    md_content = """
## Section 1: Test Section

### 1.1 Test Subsection

#### Question 1.1.1

**Question:** Do you have a security policy?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Policies are important.

**Answer Options:**

**Option 1:** Yes, documented and approved

**Option 2:** Yes, but not approved

**Option 3:** No
"""

    structure = parse_assessment_questions(md_content)

    assert len(structure.sections) == 1
    assert len(structure.sections[0].questions) == 1

    question = structure.sections[0].questions[0]
    assert len(question.options) == 3
    assert question.options[0].value == "1"
    assert question.options[0].label == "Yes, documented and approved"
    assert question.options[1].value == "2"
    assert question.options[1].label == "Yes, but not approved"
    assert question.options[2].value == "3"
    assert question.options[2].label == "No"


def test_parse_mixed_format_options() -> None:
    """Test parsing document with both slug and numeric formats"""
    md_content = """
## Section 1: Test Section

### 1.1 Test Subsection

#### Question 1.1.1

**Question:** Question with slugs?

**Type:** multiple_choice

**Scale:** maturity

**Answer Options:**

**Option optimized:** Optimized

**Option managed:** Managed

#### Question 1.1.2

**Question:** Question with numbers?

**Type:** multiple_choice

**Answer Options:**

**Option 1:** First option

**Option 2:** Second option
"""

    structure = parse_assessment_questions(md_content)

    assert len(structure.sections) == 1
    assert len(structure.sections[0].questions) == 2

    q1 = structure.sections[0].questions[0]
    assert q1.options[0].value == "optimized"
    assert q1.options[1].value == "managed"

    q2 = structure.sections[0].questions[1]
    assert q2.options[0].value == "1"
    assert q2.options[1].value == "2"
