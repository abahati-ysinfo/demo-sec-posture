from typing import Any
from unittest.mock import MagicMock, patch

from app.schemas.assessment import Question, QuestionOption
from app.services.report_generator import (
    calculate_assessment_scores,
    calculate_confidence_level,
    calculate_question_score,
    generate_ai_insights,
    generate_prioritized_remediation,
    generate_section_summaries,
    get_maturity_tier,
    normalize_answer_display,
)


def test_calculate_question_score_yes() -> None:
    from app.models.assessment import AssessmentResponse

    response = MagicMock(spec=AssessmentResponse)
    response.answer_value = "yes"

    question = MagicMock(spec=Question)
    question.type = "yes_no"
    question.weight = 5

    score = calculate_question_score(response, question)
    assert score == 5


def test_calculate_question_score_no() -> None:
    from app.models.assessment import AssessmentResponse

    response = MagicMock(spec=AssessmentResponse)
    response.answer_value = "no"

    question = MagicMock(spec=Question)
    question.type = "yes_no"
    question.weight = 5

    score = calculate_question_score(response, question)
    assert score == 0


def test_calculate_question_score_multiple_choice() -> None:
    from app.models.assessment import AssessmentResponse

    response = MagicMock(spec=AssessmentResponse)
    response.answer_value = "option1"

    question = MagicMock(spec=Question)
    question.type = "multiple_choice"
    question.weight = 3

    score = calculate_question_score(response, question)
    assert score == 3


def test_calculate_question_score_na() -> None:
    from app.models.assessment import AssessmentResponse

    response = MagicMock(spec=AssessmentResponse)
    response.answer_value = "n/a"

    question = MagicMock(spec=Question)
    question.type = "yes_no"
    question.weight = 5

    score = calculate_question_score(response, question)
    assert score == 0


def test_calculate_assessment_scores(test_assessment_response: Any) -> None:
    from app.services.question_parser import load_assessment_structure

    structure = load_assessment_structure()
    responses = [test_assessment_response]

    scores = calculate_assessment_scores(responses, structure)

    assert scores is not None
    assert "overall" in scores
    assert scores["overall"]["score"] >= 0
    assert scores["overall"]["max_score"] > 0


def test_calculate_assessment_scores_empty() -> None:
    from app.services.question_parser import load_assessment_structure

    structure = load_assessment_structure()
    responses: list[Any] = []

    scores = calculate_assessment_scores(responses, structure)

    assert scores["overall"]["score"] == 0
    assert scores["overall"]["max_score"] > 0


def test_generate_ai_insights(encryption_key: str, mocker: Any) -> None:
    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key = mocker.MagicMock()
    mock_key.id = "test-key-id"
    mock_key.encrypted_key = encrypt_api_key("test-api-key")
    mock_key.is_active = True
    mock_key.cooldown_until = None
    mock_key.last_used_at = None
    mock_key.usage_count = 0
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = '{"schema_version": "1.0", "risk_level": "Low", "risk_explanation": "Test insight", "strengths": ["Good"], "gaps": [], "recommendations": [], "benchmarks": [], "confidence_score": 0.8}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)


def test_generate_standard_report(
    db_session: Any,
    test_report: Any,
    completed_assessment: Any,
    test_assessment_response: Any,
) -> None:
    from app.services.report_generator import generate_standard_report

    with patch("app.services.report_generator.HTML") as mock_html_class:
        mock_html_instance = MagicMock()
        mock_html_class.return_value = mock_html_instance
        mock_html_instance.write_pdf = MagicMock(return_value=b"pdf-bytes")

        with patch(
            "app.services.report_generator.get_storage_service"
        ) as mock_storage_factory:
            mock_storage = MagicMock()
            mock_storage.save.return_value = "/tmp/report.pdf"
            mock_storage.exists.return_value = True
            mock_storage_factory.return_value = mock_storage

            generate_standard_report(str(test_report.id))

            mock_storage.save.assert_called_once()

    db_session.refresh(test_report)


def test_generate_ai_report(
    encryption_key: str,
    db_session: Any,
    completed_assessment: Any,
    test_assessment_response: Any,
) -> None:
    from app.models.assessment import Report
    from app.services.report_generator import generate_ai_report

    ai_report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="pending",
    )
    db_session.add(ai_report)
    db_session.commit()
    db_session.refresh(ai_report)

    with patch(
        "app.services.report_generator.OpenAIKeyManager"
    ) as mock_key_manager_class:
        mock_key_manager = MagicMock()
        mock_key_manager_class.return_value = mock_key_manager
        mock_key_manager.get_next_key.return_value = ("test-key-id", "test-api-key")

        with patch("app.services.report_generator.OpenAI") as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "AI insights"
            mock_client.chat.completions.create.return_value = mock_response

            with patch("app.services.report_generator.HTML") as mock_html_class:
                mock_html_instance = MagicMock()
                mock_html_class.return_value = mock_html_instance
                mock_html_instance.write_pdf = MagicMock(return_value=b"pdf-bytes")

                with patch(
                    "app.services.report_generator.get_storage_service"
                ) as mock_storage_factory:
                    mock_storage = MagicMock()
                    mock_storage.save.return_value = "/tmp/ai-report.pdf"
                    mock_storage.exists.return_value = True
                    mock_storage_factory.return_value = mock_storage

                    generate_ai_report(str(ai_report.id))

                    mock_storage.save.assert_called_once()

            db_session.refresh(ai_report)


def test_format_responses_for_ai() -> None:
    from app.services.report_generator import format_responses_for_ai

    responses = [
        {"question": "Test question 1?", "answer": "yes", "weight": 5},
        {"question": "Test question 2?", "answer": "no", "weight": 3},
    ]

    result = format_responses_for_ai(responses)

    assert "Test question 1?" in result
    assert "yes" in result
    assert "Weight: 5" in result
    assert "Test question 2?" in result
    assert "no" in result
    assert "Weight: 3" in result


def test_generate_recommendations() -> None:
    from app.services.question_parser import create_sample_assessment_structure
    from app.services.report_generator import generate_recommendations

    structure = create_sample_assessment_structure()

    scores = {
        "overall": {"percentage": 50.0},
        "section_1": {"percentage": 40.0},
        "section_2": {"percentage": 60.0},
    }

    recommendations = generate_recommendations(scores, structure)

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0


def test_generate_recommendations_high_score() -> None:
    from app.services.question_parser import create_sample_assessment_structure
    from app.services.report_generator import generate_recommendations

    structure = create_sample_assessment_structure()

    scores = {
        "overall": {"percentage": 85.0},
        "section_1": {"percentage": 90.0},
        "section_2": {"percentage": 85.0},
    }

    recommendations = generate_recommendations(scores, structure)

    assert isinstance(recommendations, list)


def test_generate_report_html(
    completed_assessment: Any, test_assessment_response: Any
) -> None:
    from app.services.question_parser import create_sample_assessment_structure
    from app.services.report_generator import generate_report_html

    structure = create_sample_assessment_structure()
    responses = [test_assessment_response]
    scores = {
        "overall": {"percentage": 75.0, "score": 75, "max_score": 100},
        "section_1": {
            "percentage": 70.0,
            "score": 70,
            "max_score": 100,
            "completion_rate": 80.0,
            "responses_count": 4,
            "total_questions": 5,
        },
        "section_2": {
            "percentage": 80.0,
            "score": 80,
            "max_score": 100,
            "completion_rate": 90.0,
            "responses_count": 9,
            "total_questions": 10,
        },
    }

    html = generate_report_html(completed_assessment, responses, scores, structure)

    assert isinstance(html, str)
    assert "Security Posture Assessment Report" in html
    assert "75.0%" in html
    assert len(html) > 100


def test_generate_ai_report_html(
    completed_assessment: Any, test_assessment_response: Any
) -> None:
    from app.schemas.ai_artifacts import (
        Benchmark,
        Gap,
        Recommendation,
        SectionAIArtifact,
    )
    from app.services.question_parser import create_sample_assessment_structure
    from app.services.report_generator import generate_ai_report_html

    structure = create_sample_assessment_structure()
    responses = [test_assessment_response]
    scores = {
        "overall": {"percentage": 75.0, "score": 75, "max_score": 100},
        "section_1": {
            "percentage": 70.0,
            "score": 70,
            "max_score": 100,
            "completion_rate": 80.0,
            "responses_count": 4,
            "total_questions": 5,
        },
        "section_2": {
            "percentage": 80.0,
            "score": 80,
            "max_score": 100,
            "completion_rate": 90.0,
            "responses_count": 9,
            "total_questions": 10,
        },
    }
    ai_insights = {
        "section_1": SectionAIArtifact(
            schema_version="1.0",
            risk_level="Medium",
            risk_explanation="Good progress in this area but some gaps remain that need attention",
            strengths=["Strong authentication", "Regular updates"],
            gaps=[Gap(gap="Missing MFA", linked_signals=["Q1"], severity="High")],
            recommendations=[
                Recommendation(
                    action="Implement MFA",
                    rationale="Multi-factor authentication will significantly improve account security and prevent unauthorized access",
                    linked_signals=["Q1"],
                    effort="Medium",
                    impact="High",
                    timeline="30-day",
                    references=["NIST CSF PR.AC-7"],
                )
            ],
            benchmarks=[
                Benchmark(
                    control="Multi-Factor Authentication",
                    status="Partial",
                    framework="NIST",
                    reference="PR.AC-7",
                )
            ],
            confidence_score=0.85,
        ),
        "section_2": SectionAIArtifact(
            schema_version="1.0",
            risk_level="Low",
            risk_explanation="Excellent security practices are in place with comprehensive coverage",
            strengths=["Comprehensive policies", "Regular audits"],
            gaps=[
                Gap(
                    gap="Minor documentation gaps in incident response procedures",
                    linked_signals=["Q2"],
                    severity="Low",
                )
            ],
            recommendations=[
                Recommendation(
                    action="Update incident response documentation",
                    rationale="Keeping documentation current ensures team readiness and compliance with best practices",
                    linked_signals=["Q2"],
                    effort="Low",
                    impact="Low",
                    timeline="90-day",
                    references=["ISO 27001 A.16.1.5"],
                )
            ],
            benchmarks=[
                Benchmark(
                    control="Security Policies",
                    status="Implemented",
                    framework="ISO",
                    reference="A.5.1.1",
                )
            ],
            confidence_score=0.9,
        ),
    }

    html = generate_ai_report_html(
        completed_assessment, responses, scores, structure, ai_insights
    )

    assert isinstance(html, str)
    assert "AI-Enhanced Security Posture Assessment Report" in html
    assert "75.0%" in html
    assert "Good progress" in html
    assert len(html) > 100


def test_normalize_answer_display_yes_no() -> None:
    question = MagicMock(spec=Question)
    question.type = "yes_no"

    assert normalize_answer_display(True, question) == "Yes"
    assert normalize_answer_display(False, question) == "No"
    assert normalize_answer_display("yes", question) == "Yes"
    assert normalize_answer_display("no", question) == "No"
    assert normalize_answer_display("YES", question) == "Yes"
    assert normalize_answer_display(None, question) == "Not answered"


def test_normalize_answer_display_multiple_choice() -> None:
    option1 = QuestionOption(
        value="opt1", label="Option One", description="First option"
    )
    option2 = QuestionOption(
        value="opt2", label="Option Two", description="Second option"
    )

    question = MagicMock(spec=Question)
    question.type = "multiple_choice"
    question.options = [option1, option2]

    assert normalize_answer_display("opt1", question) == "Option One"
    assert normalize_answer_display("opt2", question) == "Option Two"
    assert normalize_answer_display("unknown", question) == "unknown"
    assert normalize_answer_display(None, question) == "Not answered"


def test_normalize_answer_display_multiple_select() -> None:
    option1 = QuestionOption(
        value="opt1", label="Option One", description="First option"
    )
    option2 = QuestionOption(
        value="opt2", label="Option Two", description="Second option"
    )

    question = MagicMock(spec=Question)
    question.type = "multiple_select"
    question.options = [option1, option2]

    assert (
        normalize_answer_display(["opt1", "opt2"], question) == "Option One, Option Two"
    )
    assert normalize_answer_display(["opt1"], question) == "Option One"
    assert normalize_answer_display([], question) == "Not answered"
    assert normalize_answer_display(None, question) == "Not answered"


def test_normalize_answer_display_text() -> None:
    question = MagicMock(spec=Question)
    question.type = "text"

    assert normalize_answer_display("Some text", question) == "Some text"
    assert normalize_answer_display("Line 1\nLine 2", question) == "Line 1<br>Line 2"
    assert normalize_answer_display("", question) == "Not answered"
    assert normalize_answer_display("   ", question) == "Not answered"
    assert normalize_answer_display(None, question) == "Not answered"


def test_get_maturity_tier() -> None:
    tier, css = get_maturity_tier(80.0)
    assert tier == "Strong"
    assert css == "high-score"

    tier, css = get_maturity_tier(60.0)
    assert tier == "Moderate"
    assert css == "medium-score"

    tier, css = get_maturity_tier(59.9)
    assert tier == "Needs Improvement"
    assert css == "low-score"

    tier, css = get_maturity_tier(100.0)
    assert tier == "Strong"

    tier, css = get_maturity_tier(0.0)
    assert tier == "Needs Improvement"


def test_calculate_confidence_level_high() -> None:
    scores = {
        "overall": {"percentage": 85.0},
        "section_1": {"percentage": 80.0, "completion_rate": 85.0},
        "section_2": {"percentage": 90.0, "completion_rate": 90.0},
    }

    level, description = calculate_confidence_level(scores)
    assert level == "High"
    assert "substantially completed" in description


def test_calculate_confidence_level_medium() -> None:
    scores = {
        "overall": {"percentage": 70.0},
        "section_1": {"percentage": 65.0, "completion_rate": 65.0},
        "section_2": {"percentage": 75.0, "completion_rate": 70.0},
    }

    level, description = calculate_confidence_level(scores)
    assert level == "Medium"
    assert "generally reliable" in description


def test_calculate_confidence_level_low() -> None:
    scores = {
        "overall": {"percentage": 50.0},
        "section_1": {"percentage": 40.0, "completion_rate": 50.0},
        "section_2": {"percentage": 60.0, "completion_rate": 55.0},
    }

    level, description = calculate_confidence_level(scores)
    assert level == "Low"
    assert "gaps" in description


def test_generate_prioritized_remediation() -> None:
    from app.services.question_parser import create_sample_assessment_structure

    structure = create_sample_assessment_structure()
    scores = {
        "section_1": {"percentage": 45.0},
        "section_2": {"percentage": 65.0},
    }

    items = generate_prioritized_remediation(scores, structure)

    assert isinstance(items, list)
    assert len(items) > 0

    p1_item = items[0]
    assert p1_item["priority"] == "P1"
    assert p1_item["effort"] == "Medium"
    assert p1_item["timeframe"] == "30-90 days"
    assert "45.0%" in p1_item["current_score"]

    p2_item = items[1]
    assert p2_item["priority"] == "P2"
    assert p2_item["effort"] == "Medium"
    assert p2_item["timeframe"] == "30-90 days"


def test_generate_section_summaries() -> None:
    from app.models.assessment import AssessmentResponse
    from app.services.question_parser import create_sample_assessment_structure

    structure = create_sample_assessment_structure()

    response1 = MagicMock(spec=AssessmentResponse)
    response1.question_id = "1_1_1"
    response1.answer_value = "yes"
    response1.comment = None

    response2 = MagicMock(spec=AssessmentResponse)
    response2.question_id = "1_1_2"
    response2.answer_value = "annually"
    response2.comment = "We review annually"

    responses = [response1, response2]

    scores = {
        "section_1": {
            "percentage": 85.0,
            "completion_rate": 100.0,
            "responses_count": 2,
            "total_questions": 2,
        },
        "section_2": {
            "percentage": 60.0,
            "completion_rate": 50.0,
            "responses_count": 1,
            "total_questions": 2,
        },
    }

    summaries = generate_section_summaries(scores, structure, responses)

    assert isinstance(summaries, list)
    assert len(summaries) == 2

    summary1 = summaries[0]
    assert summary1["score"] == 85.0
    assert summary1["completion"] == 100.0
    assert len(summary1["strengths"]) >= 0
    assert len(summary1["recommendations"]) > 0


def test_generate_report_html_enhanced(
    completed_assessment: Any, test_assessment_response: Any
) -> None:
    from app.models.assessment import AssessmentResponse
    from app.services.question_parser import create_sample_assessment_structure
    from app.services.report_generator import generate_report_html

    structure = create_sample_assessment_structure()

    completed_assessment.consultation_interest = True
    completed_assessment.consultation_details = (
        "We need help with security improvements"
    )
    completed_assessment.progress_percentage = 65.0

    response_with_comment = MagicMock(spec=AssessmentResponse)
    response_with_comment.question_id = "1_1_1"
    response_with_comment.answer_value = "yes"
    response_with_comment.comment = "This is a test comment"

    responses = [test_assessment_response, response_with_comment]

    scores = {
        "overall": {"percentage": 65.0, "score": 65, "max_score": 100},
        "section_1": {
            "percentage": 60.0,
            "score": 60,
            "max_score": 100,
            "completion_rate": 75.0,
            "responses_count": 3,
            "total_questions": 4,
        },
        "section_2": {
            "percentage": 70.0,
            "score": 70,
            "max_score": 100,
            "completion_rate": 80.0,
            "responses_count": 4,
            "total_questions": 5,
        },
    }

    html = generate_report_html(completed_assessment, responses, scores, structure)

    assert isinstance(html, str)
    assert "Table of Contents" in html
    assert "Methodology and Scoring" in html
    assert "Data Quality and Confidence Level" in html
    assert "Domain Heatmap and Maturity Tiers" in html
    assert "Prioritized Remediation Plan" in html
    assert "Section Summaries" in html
    assert "Detailed Responses (All Questions and Answers)" in html
    assert "Comments Digest" in html
    assert "Consultation Interest:" in html
    assert "We need help with security improvements" in html
    assert "Not answered" in html
    assert "Disclaimer" in html


def test_generate_ai_insights_validation_error(
    encryption_key: str, mocker: Any
) -> None:
    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key = mocker.MagicMock()
    mock_key.id = "test-key-id"
    mock_key.encrypted_key = encrypt_api_key("test-api-key")
    mock_key.is_active = True
    mock_key.cooldown_until = None
    mock_key.last_used_at = None
    mock_key.usage_count = 0
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"invalid": "json"}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Medium"
            assert "temporarily unavailable" in artifact.risk_explanation


def test_generate_ai_insights_authentication_error(
    encryption_key: str, mocker: Any
) -> None:
    from openai import AuthenticationError

    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key = mocker.MagicMock()
    mock_key.id = "test-key-id"
    mock_key.encrypted_key = encrypt_api_key("test-api-key")
    mock_key.is_active = True
    mock_key.cooldown_until = None
    mock_key.last_used_at = None
    mock_key.usage_count = 0
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_client.chat.completions.create.side_effect = AuthenticationError(
            "Invalid API key", response=MagicMock(), body=None
        )

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Medium"
            assert "temporarily unavailable" in artifact.risk_explanation


def test_generate_ai_insights_rate_limit_error(
    encryption_key: str, mocker: Any
) -> None:
    from openai import RateLimitError

    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key = mocker.MagicMock()
    mock_key.id = "test-key-id"
    mock_key.encrypted_key = encrypt_api_key("test-api-key")
    mock_key.is_active = True
    mock_key.cooldown_until = None
    mock_key.last_used_at = None
    mock_key.usage_count = 0
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_client.chat.completions.create.side_effect = RateLimitError(
            "Rate limit exceeded", response=MagicMock(), body=None
        )

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Medium"
            assert "temporarily unavailable" in artifact.risk_explanation


def test_generate_ai_insights_api_connection_error(
    encryption_key: str, mocker: Any
) -> None:
    from openai import APIConnectionError

    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key = mocker.MagicMock()
    mock_key.id = "test-key-id"
    mock_key.encrypted_key = encrypt_api_key("test-api-key")
    mock_key.is_active = True
    mock_key.cooldown_until = None
    mock_key.last_used_at = None
    mock_key.usage_count = 0
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_request = MagicMock()
        mock_client.chat.completions.create.side_effect = APIConnectionError(
            message="Connection failed", request=mock_request
        )

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Medium"
            assert "temporarily unavailable" in artifact.risk_explanation


def test_generate_ai_insights_sqlalchemy_error(
    encryption_key: str, mocker: Any
) -> None:
    from sqlalchemy.exc import SQLAlchemyError

    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key = mocker.MagicMock()
    mock_key.id = "test-key-id"
    mock_key.encrypted_key = encrypt_api_key("test-api-key")
    mock_key.is_active = True
    mock_key.cooldown_until = None
    mock_key.last_used_at = None
    mock_key.usage_count = 0
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_key

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = '{"schema_version": "1.0", "risk_level": "Low", "risk_explanation": "Test insight with sufficient length for validation", "strengths": ["Good security practices"], "gaps": [{"gap": "Minor gap found", "linked_signals": ["Q1"], "severity": "Low"}], "recommendations": [{"action": "Implement security controls", "rationale": "This is a detailed rationale explaining why this action is important", "linked_signals": ["Q1"], "effort": "Low", "impact": "Medium", "timeline": "30-day", "references": []}], "benchmarks": [{"control": "Test Control", "status": "Implemented", "framework": "NIST", "reference": ""}], "confidence_score": 0.8}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response

        mock_db.add.side_effect = SQLAlchemyError("Database error")

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Medium"
            assert "temporarily unavailable" in artifact.risk_explanation


def test_generate_ai_insights_authentication_error_with_retry(
    encryption_key: str, mocker: Any
) -> None:
    from openai import AuthenticationError

    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key1 = mocker.MagicMock()
    mock_key1.id = "test-key-1"
    mock_key1.encrypted_key = encrypt_api_key("test-api-key-1")
    mock_key1.is_active = True
    mock_key1.cooldown_until = None
    mock_key1.last_used_at = None
    mock_key1.usage_count = 0

    mock_key2 = mocker.MagicMock()
    mock_key2.id = "test-key-2"
    mock_key2.encrypted_key = encrypt_api_key("test-api-key-2")
    mock_key2.is_active = True
    mock_key2.cooldown_until = None
    mock_key2.last_used_at = None
    mock_key2.usage_count = 0

    mock_db.query.return_value.filter.return_value.order_by.return_value.first.side_effect = [
        mock_key1,
        mock_key2,
    ]

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()

        call_count = [0]

        def create_client_side_effect(*args: Any, **kwargs: Any) -> Any:
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_client1
            else:
                return mock_client2

        mock_openai_class.side_effect = create_client_side_effect

        mock_client1.chat.completions.create.side_effect = AuthenticationError(
            "Invalid API key", response=MagicMock(), body=None
        )

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = '{"schema_version": "1.0", "risk_level": "Low", "risk_explanation": "Test insight with sufficient length for validation", "strengths": ["Good security practices"], "gaps": [{"gap": "Minor gap found", "linked_signals": ["Q1"], "severity": "Low"}], "recommendations": [{"action": "Implement security controls", "rationale": "This is a detailed rationale explaining why this action is important", "linked_signals": ["Q1"], "effort": "Low", "impact": "Medium", "timeline": "30-day", "references": []}], "benchmarks": [{"control": "Test Control", "status": "Implemented", "framework": "NIST", "reference": ""}], "confidence_score": 0.8}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client2.chat.completions.create.return_value = mock_response

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Low"
            assert "Test insight" in artifact.risk_explanation


def test_generate_ai_insights_rate_limit_error_with_retry(
    encryption_key: str, mocker: Any
) -> None:
    from openai import RateLimitError

    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key1 = mocker.MagicMock()
    mock_key1.id = "test-key-1"
    mock_key1.encrypted_key = encrypt_api_key("test-api-key-1")
    mock_key1.is_active = True
    mock_key1.cooldown_until = None
    mock_key1.last_used_at = None
    mock_key1.usage_count = 0

    mock_key2 = mocker.MagicMock()
    mock_key2.id = "test-key-2"
    mock_key2.encrypted_key = encrypt_api_key("test-api-key-2")
    mock_key2.is_active = True
    mock_key2.cooldown_until = None
    mock_key2.last_used_at = None
    mock_key2.usage_count = 0

    mock_db.query.return_value.filter.return_value.order_by.return_value.first.side_effect = [
        mock_key1,
        mock_key2,
    ]

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()

        call_count = [0]

        def create_client_side_effect(*args: Any, **kwargs: Any) -> Any:
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_client1
            else:
                return mock_client2

        mock_openai_class.side_effect = create_client_side_effect

        mock_client1.chat.completions.create.side_effect = RateLimitError(
            "Rate limit exceeded", response=MagicMock(), body=None
        )

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = '{"schema_version": "1.0", "risk_level": "Low", "risk_explanation": "Test insight with sufficient length for validation", "strengths": ["Good security practices"], "gaps": [{"gap": "Minor gap found", "linked_signals": ["Q1"], "severity": "Low"}], "recommendations": [{"action": "Implement security controls", "rationale": "This is a detailed rationale explaining why this action is important", "linked_signals": ["Q1"], "effort": "Low", "impact": "Medium", "timeline": "30-day", "references": []}], "benchmarks": [{"control": "Test Control", "status": "Implemented", "framework": "NIST", "reference": ""}], "confidence_score": 0.8}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client2.chat.completions.create.return_value = mock_response

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Low"
            assert "Test insight" in artifact.risk_explanation


def test_generate_ai_insights_api_error_with_retry(
    encryption_key: str, mocker: Any
) -> None:
    from openai import APIConnectionError

    from app.services.openai_key_manager import OpenAIKeyManager
    from app.services.question_parser import create_sample_assessment_structure
    from app.utils.encryption import encrypt_api_key

    structure = create_sample_assessment_structure()
    responses: list[Any] = []

    mock_db = mocker.MagicMock()
    key_manager = OpenAIKeyManager(mock_db)

    mock_key1 = mocker.MagicMock()
    mock_key1.id = "test-key-1"
    mock_key1.encrypted_key = encrypt_api_key("test-api-key-1")
    mock_key1.is_active = True
    mock_key1.cooldown_until = None
    mock_key1.last_used_at = None
    mock_key1.usage_count = 0

    mock_key2 = mocker.MagicMock()
    mock_key2.id = "test-key-2"
    mock_key2.encrypted_key = encrypt_api_key("test-api-key-2")
    mock_key2.is_active = True
    mock_key2.cooldown_until = None
    mock_key2.last_used_at = None
    mock_key2.usage_count = 0

    mock_db.query.return_value.filter.return_value.order_by.return_value.first.side_effect = [
        mock_key1,
        mock_key2,
    ]

    with patch("app.services.report_generator.OpenAI") as mock_openai_class:
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()

        call_count = [0]

        def create_client_side_effect(*args: Any, **kwargs: Any) -> Any:
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_client1
            else:
                return mock_client2

        mock_openai_class.side_effect = create_client_side_effect

        mock_request = MagicMock()
        mock_client1.chat.completions.create.side_effect = APIConnectionError(
            message="Connection failed", request=mock_request
        )

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = '{"schema_version": "1.0", "risk_level": "Low", "risk_explanation": "Test insight with sufficient length for validation", "strengths": ["Good security practices"], "gaps": [{"gap": "Minor gap found", "linked_signals": ["Q1"], "severity": "Low"}], "recommendations": [{"action": "Implement security controls", "rationale": "This is a detailed rationale explaining why this action is important", "linked_signals": ["Q1"], "effort": "Low", "impact": "Medium", "timeline": "30-day", "references": []}], "benchmarks": [{"control": "Test Control", "status": "Implemented", "framework": "NIST", "reference": ""}], "confidence_score": 0.8}'
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client2.chat.completions.create.return_value = mock_response

        insights = generate_ai_insights(
            responses, structure, key_manager, "test-report-id", mock_db
        )

        assert insights is not None
        assert isinstance(insights, dict)
        for _section_id, artifact in insights.items():
            assert artifact.risk_level == "Low"
            assert "Test insight" in artifact.risk_explanation


def test_create_degraded_artifact() -> None:
    from app.services.report_generator import create_degraded_artifact

    artifact = create_degraded_artifact("test-section-id")

    assert artifact is not None
    assert artifact.risk_level == "Medium"
    assert "temporarily unavailable" in artifact.risk_explanation
    assert len(artifact.strengths) == 1
    assert "Assessment data collected successfully" in artifact.strengths[0]
    assert len(artifact.gaps) == 1
    assert artifact.gaps[0].gap == "AI analysis unavailable"
    assert artifact.gaps[0].severity == "Low"
    assert len(artifact.recommendations) == 1
    assert "Retry" in artifact.recommendations[0].action
    assert len(artifact.benchmarks) == 1
    assert artifact.benchmarks[0].status == "Implemented"
    assert artifact.confidence_score == 0.0
