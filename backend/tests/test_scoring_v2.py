"""
Tests for scoring v2 with weighted scales
"""

from unittest.mock import Mock

from app.core.scoring_scales import map_numeric_to_slug
from app.models.assessment import AssessmentResponse
from app.schemas.assessment import Question, QuestionOption
from app.services.report_generator import calculate_question_score_v2


def create_test_question(scale_type: str, weight: int = 10) -> Question:
    """Helper to create a test question"""
    return Question(
        id="test_q",
        section_id="test_s",
        text="Test question",
        type="multiple_choice",
        weight=weight,
        explanation="Test",
        options=[],
        metadata={"scale_type": scale_type},
    )


def create_test_response(answer_value: str) -> AssessmentResponse:
    """Helper to create a test response"""
    response = Mock(spec=AssessmentResponse)
    response.question_id = "test_q"
    response.answer_value = answer_value
    return response


class TestMaturityScale:
    """Test maturity scale scoring"""

    def test_optimized_gets_full_weight(self) -> None:
        question = create_test_question("maturity", weight=10)
        response = create_test_response("optimized")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_managed_gets_75_percent(self) -> None:
        question = create_test_question("maturity", weight=10)
        response = create_test_response("managed")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 7
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_defined_gets_50_percent(self) -> None:
        question = create_test_question("maturity", weight=10)
        response = create_test_response("defined")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 5
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_ad_hoc_gets_25_percent(self) -> None:
        question = create_test_question("maturity", weight=10)
        response = create_test_response("ad_hoc")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 2
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestFrequencyReviewScale:
    """Test frequency_review scale scoring"""

    def test_quarterly_gets_full_weight(self) -> None:
        question = create_test_question("frequency_review", weight=10)
        response = create_test_response("quarterly")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_annually_gets_75_percent(self) -> None:
        question = create_test_question("frequency_review", weight=10)
        response = create_test_response("annually")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 7
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_only_after_changes_gets_50_percent(self) -> None:
        question = create_test_question("frequency_review", weight=10)
        response = create_test_response("only_after_changes")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 5
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_no_formal_review_gets_zero(self) -> None:
        question = create_test_question("frequency_review", weight=10)
        response = create_test_response("no_formal_review")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 0
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestCoverageScale:
    """Test coverage scale scoring"""

    def test_76_100_gets_full_weight(self) -> None:
        question = create_test_question("coverage", weight=10)
        response = create_test_response("76_100")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_51_75_gets_75_percent(self) -> None:
        question = create_test_question("coverage", weight=10)
        response = create_test_response("51_75")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 7
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestImplementationScale:
    """Test implementation scale scoring"""

    def test_fully_implemented_gets_full_weight(self) -> None:
        question = create_test_question("implementation", weight=10)
        response = create_test_response("fully_implemented")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_partially_implemented_gets_50_percent(self) -> None:
        question = create_test_question("implementation", weight=10)
        response = create_test_response("partially_implemented")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 5
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_planned_gets_25_percent(self) -> None:
        question = create_test_question("implementation", weight=10)
        response = create_test_response("planned")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 2
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_not_implemented_gets_zero(self) -> None:
        question = create_test_question("implementation", weight=10)
        response = create_test_response("not_implemented")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 0
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestGovernanceScale:
    """Test governance scale scoring"""

    def test_documented_approved_maintained_gets_full_weight(self) -> None:
        question = create_test_question("governance", weight=10)
        response = create_test_response("documented_approved_maintained")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_documented_but_stale_gets_50_percent(self) -> None:
        question = create_test_question("governance", weight=10)
        response = create_test_response("documented_but_stale")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 5
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_informal_understanding_gets_25_percent(self) -> None:
        question = create_test_question("governance", weight=10)
        response = create_test_response("informal_understanding")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 2
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_no_strategy_gets_zero(self) -> None:
        question = create_test_question("governance", weight=10)
        response = create_test_response("no_strategy")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 0
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestSpecialHandling:
    """Test special handling for unknown and not_applicable"""

    def test_unknown_gets_flagged(self) -> None:
        question = create_test_question("maturity", weight=10)
        response = create_test_response("not_sure")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 0
        assert result["max_score"] == 10
        assert "unknown" in result["flags"]

    def test_not_applicable_excluded_from_denominator(self) -> None:
        question = create_test_question("maturity", weight=10)
        response = create_test_response("not_applicable")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 0
        assert result["max_score"] == 0
        assert "not_applicable" in result["flags"]

    def test_unknown_variants_all_flagged(self) -> None:
        question = create_test_question("maturity", weight=10)

        for variant in ["unknown", "not_sure", "don't_know"]:
            response = create_test_response(variant)
            result = calculate_question_score_v2(response, question)

            assert "unknown" in result["flags"], f"Failed for variant: {variant}"

    def test_not_applicable_variants_all_flagged(self) -> None:
        question = create_test_question("maturity", weight=10)

        for variant in ["not_applicable", "n/a", "na"]:
            response = create_test_response(variant)
            result = calculate_question_score_v2(response, question)

            assert "not_applicable" in result["flags"], f"Failed for variant: {variant}"


class TestYesNoQuestions:
    """Test yes/no question scoring"""

    def test_yes_gets_full_weight(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test question",
            type="yes_no",
            weight=10,
            explanation="Test",
            options=[],
            metadata={},
        )
        response = create_test_response("yes")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_no_gets_zero(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test question",
            type="yes_no",
            weight=10,
            explanation="Test",
            options=[],
            metadata={},
        )
        response = create_test_response("no")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 0
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestMultipleSelectQuestions:
    """Test multiple_select question scoring"""

    def test_best_answer_wins(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test question",
            type="multiple_select",
            weight=10,
            explanation="Test",
            options=[],
            metadata={"scale_type": "maturity"},
        )
        response = Mock(spec=AssessmentResponse)
        response.question_id = "test_q"
        response.answer_value = ["ad_hoc", "managed", "defined"]

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 7
        assert result["max_score"] == 10
        assert result["flags"] == []

    def test_empty_list_gets_zero(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test question",
            type="multiple_select",
            weight=10,
            explanation="Test",
            options=[],
            metadata={"scale_type": "maturity"},
        )
        response = Mock(spec=AssessmentResponse)
        response.question_id = "test_q"
        response.answer_value = []

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 0
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestFallbackBehavior:
    """Test fallback behavior for questions without scale_type"""

    def test_no_scale_type_uses_v1_logic(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test question",
            type="multiple_choice",
            weight=10,
            explanation="Test",
            options=[],
            metadata={},
        )
        response = create_test_response("any_answer")

        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10
        assert result["flags"] == []


class TestNumericToSlugMapper:
    """Test runtime numeric→slug mapper for Phase 3a"""

    def test_slug_value_returns_unchanged(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test",
            type="multiple_choice",
            weight=10,
            explanation="Test",
            options=[
                QuestionOption(value="quarterly", label="Quarterly", description=""),
                QuestionOption(value="annually", label="Annually", description=""),
            ],
            metadata={},
        )

        result = map_numeric_to_slug(question, "quarterly")
        assert result == "quarterly"

    def test_numeric_value_maps_to_slug(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test",
            type="multiple_choice",
            weight=10,
            explanation="Test",
            options=[
                QuestionOption(value="quarterly", label="Quarterly", description=""),
                QuestionOption(value="annually", label="Annually", description=""),
                QuestionOption(value="never", label="Never", description=""),
            ],
            metadata={},
        )

        assert map_numeric_to_slug(question, "1") == "quarterly"
        assert map_numeric_to_slug(question, "2") == "annually"
        assert map_numeric_to_slug(question, "3") == "never"

    def test_numeric_value_with_numeric_options(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test",
            type="multiple_choice",
            weight=10,
            explanation="Test",
            options=[
                QuestionOption(value="1", label="First", description=""),
                QuestionOption(value="2", label="Second", description=""),
            ],
            metadata={},
        )

        assert map_numeric_to_slug(question, "1") == "1"
        assert map_numeric_to_slug(question, "2") == "2"

    def test_out_of_range_numeric_returns_unchanged(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test",
            type="multiple_choice",
            weight=10,
            explanation="Test",
            options=[
                QuestionOption(value="quarterly", label="Quarterly", description=""),
            ],
            metadata={},
        )

        result = map_numeric_to_slug(question, "99")
        assert result == "99"

    def test_empty_value_returns_unchanged(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test",
            type="multiple_choice",
            weight=10,
            explanation="Test",
            options=[],
            metadata={},
        )

        assert map_numeric_to_slug(question, "") == ""
        assert map_numeric_to_slug(question, None) is None  # type: ignore[arg-type]

    def test_scoring_with_numeric_values_uses_mapper(self) -> None:
        question = Question(
            id="test_q",
            section_id="test_s",
            text="Test",
            type="multiple_choice",
            weight=10,
            explanation="Test",
            options=[
                QuestionOption(value="optimized", label="Optimized", description=""),
                QuestionOption(value="managed", label="Managed", description=""),
                QuestionOption(value="ad_hoc", label="Ad-hoc", description=""),
            ],
            metadata={"scale_type": "maturity"},
        )

        response = create_test_response("1")
        result = calculate_question_score_v2(response, question)

        assert result["score"] == 10
        assert result["max_score"] == 10

        response = create_test_response("2")
        result = calculate_question_score_v2(response, question)

        assert result["score"] == 7
        assert result["max_score"] == 10

        response = create_test_response("3")
        result = calculate_question_score_v2(response, question)

        assert result["score"] == 2
        assert result["max_score"] == 10
