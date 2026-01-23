"""Tests for PII redaction before AI processing"""

from typing import Any
from unittest.mock import MagicMock, patch

from app.models.assessment import AssessmentResponse
from app.services.pii_redactor import PIIRedactor
from app.services.report_generator import generate_ai_insights


class TestPIIRedactionBeforeAI:
    """Test that PII is redacted before sending to OpenAI"""

    def test_pii_redactor_redacts_email(self) -> None:
        """Test that emails are redacted"""
        redactor = PIIRedactor()
        text = "Contact me at john.doe@company.com for more info"
        redacted, count = redactor.redact(text)

        assert "john.doe@company.com" not in redacted
        assert "[EMAIL_REDACTED]" in redacted
        assert count == 1

    def test_pii_redactor_redacts_phone(self) -> None:
        """Test that phone numbers are redacted"""
        redactor = PIIRedactor()
        text = "Call me at 555-123-4567 or (555) 987-6543"
        redacted, count = redactor.redact(text)

        assert "555-123-4567" not in redacted
        assert "555-987-6543" not in redacted
        assert "[PHONE_REDACTED]" in redacted
        assert count >= 1

    def test_pii_redactor_redacts_ssn(self) -> None:
        """Test that SSNs are redacted"""
        redactor = PIIRedactor()
        text = "My SSN is 123-45-6789"
        redacted, count = redactor.redact(text)

        assert "123-45-6789" not in redacted
        assert "[SSN_REDACTED]" in redacted
        assert count == 1

    def test_pii_redactor_redacts_multiple_patterns(self) -> None:
        """Test that multiple PII patterns are redacted"""
        redactor = PIIRedactor()
        text = "Email: test@company.com, Phone: 555-123-4567, SSN: 123-45-6789"
        redacted, count = redactor.redact(text)

        assert "test@company.com" not in redacted
        assert "555-123-4567" not in redacted
        assert "123-45-6789" not in redacted
        assert "[EMAIL_REDACTED]" in redacted
        assert "[PHONE_REDACTED]" in redacted
        assert "[SSN_REDACTED]" in redacted
        assert count == 3

    def test_pii_redactor_preserves_non_pii(self) -> None:
        """Test that non-PII text is preserved"""
        redactor = PIIRedactor()
        text = "We use MFA and have strong password policies"
        redacted, count = redactor.redact(text)

        assert redacted == text
        assert count == 0

    @patch("app.services.report_generator.OpenAI")
    @patch("app.services.report_generator.OpenAIKeyManager")
    @patch("app.services.report_generator.settings")
    def test_pii_redacted_in_answers_before_ai(
        self, mock_settings: Any, mock_key_manager: Any, mock_openai: Any
    ) -> None:
        """Test that PII in answers is redacted before OpenAI API call"""
        mock_settings.ENABLE_PII_REDACTION_BEFORE_AI = True
        mock_settings.INCLUDE_COMMENTS_IN_AI = False
        mock_settings.INCLUDE_ENHANCED_CONTEXT_IN_AI = False
        mock_settings.OPENAI_MODEL = "gpt-4"
        mock_settings.OPENAI_TIMEOUT = 60
        mock_settings.OPENAI_MAX_TOKENS = 10000
        mock_settings.OPENAI_TEMPERATURE = 0.5
        mock_settings.AI_PROMPT_VERSION = "v2.3"
        mock_settings.AI_MAX_RETRIES = 3

        mock_key_manager_instance = MagicMock()
        mock_key_manager_instance.get_next_key.return_value = ("key1", "test-api-key")
        mock_key_manager.return_value = mock_key_manager_instance

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = (
            '{"summary": "test", "key_findings": [], "recommendations": [], "gaps": []}'
        )
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.choices[0].finish_reason = "stop"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        response_with_pii = AssessmentResponse(
            id="resp1",
            assessment_id="assess1",
            section_id="section1",
            question_id="q1",
            answer_value="Contact admin@company.com for access",
            comment=None,
        )

        mock_structure = MagicMock()
        mock_section = MagicMock()
        mock_section.id = "section1"
        mock_section.title = "Test Section"
        mock_section.description = "Test"
        mock_question = MagicMock()
        mock_question.id = "q1"
        mock_question.text = "Who manages access?"
        mock_question.weight = 5
        mock_section.questions = [mock_question]
        mock_structure.sections = [mock_section]

        mock_db = MagicMock()

        with patch(
            "app.services.report_generator.AICacheService"
        ) as mock_cache_service:
            mock_cache_instance = MagicMock()
            mock_cache_instance.get_cached_artifact.return_value = None
            mock_cache_instance.compute_answers_hash.return_value = "hash123"
            mock_cache_service.return_value = mock_cache_instance

            with patch(
                "app.services.report_generator.benchmark_context_service"
            ) as mock_benchmark:
                mock_benchmark.get_relevant_context.return_value = []

                with patch(
                    "app.services.report_generator.build_section_prompt_v2"
                ) as mock_build_prompt:
                    mock_build_prompt.return_value = ("test prompt", 0)

                    with patch(
                        "app.services.report_generator.safe_validate_section_artifact"
                    ) as mock_validate:
                        mock_artifact = MagicMock()
                        mock_artifact.model_dump.return_value = {"summary": "test"}
                        mock_validate.return_value = mock_artifact

                        generate_ai_insights(
                            [response_with_pii],
                            mock_structure,
                            mock_key_manager_instance,
                            "report1",
                            mock_db,
                        )

        call_args = mock_client.chat.completions.create.call_args
        assert call_args is not None

        prompt_used = mock_build_prompt.call_args[0][1][0]
        assert "admin@company.com" not in str(prompt_used.get("answer", ""))
        assert "[EMAIL_REDACTED]" in str(prompt_used.get("answer", ""))

    @patch("app.services.report_generator.OpenAI")
    @patch("app.services.report_generator.OpenAIKeyManager")
    @patch("app.services.report_generator.settings")
    def test_pii_redacted_in_comments_before_ai(
        self, mock_settings: Any, mock_key_manager: Any, mock_openai: Any
    ) -> None:
        """Test that PII in comments is redacted before OpenAI API call"""
        mock_settings.ENABLE_PII_REDACTION_BEFORE_AI = True
        mock_settings.INCLUDE_COMMENTS_IN_AI = True
        mock_settings.INCLUDE_ENHANCED_CONTEXT_IN_AI = False
        mock_settings.OPENAI_MODEL = "gpt-4"
        mock_settings.OPENAI_TIMEOUT = 60
        mock_settings.OPENAI_MAX_TOKENS = 10000
        mock_settings.OPENAI_TEMPERATURE = 0.5
        mock_settings.AI_PROMPT_VERSION = "v2.3"
        mock_settings.AI_MAX_RETRIES = 3

        mock_key_manager_instance = MagicMock()
        mock_key_manager_instance.get_next_key.return_value = ("key1", "test-api-key")
        mock_key_manager.return_value = mock_key_manager_instance

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = (
            '{"summary": "test", "key_findings": [], "recommendations": [], "gaps": []}'
        )
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.choices[0].finish_reason = "stop"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        response_with_pii_comment = AssessmentResponse(
            id="resp1",
            assessment_id="assess1",
            section_id="section1",
            question_id="q1",
            answer_value="Yes",
            comment="Call security team at 555-123-4567",
        )

        mock_structure = MagicMock()
        mock_section = MagicMock()
        mock_section.id = "section1"
        mock_section.title = "Test Section"
        mock_section.description = "Test"
        mock_question = MagicMock()
        mock_question.id = "q1"
        mock_question.text = "Do you have MFA?"
        mock_question.weight = 5
        mock_section.questions = [mock_question]
        mock_structure.sections = [mock_section]

        mock_db = MagicMock()

        with patch(
            "app.services.report_generator.AICacheService"
        ) as mock_cache_service:
            mock_cache_instance = MagicMock()
            mock_cache_instance.get_cached_artifact.return_value = None
            mock_cache_instance.compute_answers_hash.return_value = "hash123"
            mock_cache_service.return_value = mock_cache_instance

            with patch(
                "app.services.report_generator.benchmark_context_service"
            ) as mock_benchmark:
                mock_benchmark.get_relevant_context.return_value = []

                with patch(
                    "app.services.report_generator.build_section_prompt_v2"
                ) as mock_build_prompt:
                    mock_build_prompt.return_value = ("test prompt", 0)

                    with patch(
                        "app.services.report_generator.safe_validate_section_artifact"
                    ) as mock_validate:
                        mock_artifact = MagicMock()
                        mock_artifact.model_dump.return_value = {"summary": "test"}
                        mock_validate.return_value = mock_artifact

                        generate_ai_insights(
                            [response_with_pii_comment],
                            mock_structure,
                            mock_key_manager_instance,
                            "report1",
                            mock_db,
                        )

        call_args = mock_client.chat.completions.create.call_args
        assert call_args is not None

        prompt_used = mock_build_prompt.call_args[0][1][0]
        assert "555-123-4567" not in str(prompt_used.get("comment", ""))
        assert "[PHONE_REDACTED]" in str(prompt_used.get("comment", ""))

    @patch("app.services.report_generator.security_metrics")
    @patch("app.services.report_generator.OpenAI")
    @patch("app.services.report_generator.OpenAIKeyManager")
    @patch("app.services.report_generator.settings")
    def test_pii_redaction_metrics_tracked(
        self,
        mock_settings: Any,
        mock_key_manager: Any,
        mock_openai: Any,
        mock_metrics: Any,
    ) -> None:
        """Test that PII redaction events are tracked in metrics"""
        mock_settings.ENABLE_PII_REDACTION_BEFORE_AI = True
        mock_settings.INCLUDE_COMMENTS_IN_AI = True
        mock_settings.INCLUDE_ENHANCED_CONTEXT_IN_AI = False
        mock_settings.OPENAI_MODEL = "gpt-4"
        mock_settings.OPENAI_TIMEOUT = 60
        mock_settings.OPENAI_MAX_TOKENS = 10000
        mock_settings.OPENAI_TEMPERATURE = 0.5
        mock_settings.AI_PROMPT_VERSION = "v2.3"
        mock_settings.AI_MAX_RETRIES = 3

        mock_key_manager_instance = MagicMock()
        mock_key_manager_instance.get_next_key.return_value = ("key1", "test-api-key")
        mock_key_manager.return_value = mock_key_manager_instance

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = (
            '{"summary": "test", "key_findings": [], "recommendations": [], "gaps": []}'
        )
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.choices[0].finish_reason = "stop"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        response_with_pii = AssessmentResponse(
            id="resp1",
            assessment_id="assess1",
            section_id="section1",
            question_id="q1",
            answer_value="admin@company.com",
            comment="Call 555-1234",
        )

        mock_structure = MagicMock()
        mock_section = MagicMock()
        mock_section.id = "section1"
        mock_section.title = "Test Section"
        mock_section.description = "Test"
        mock_question = MagicMock()
        mock_question.id = "q1"
        mock_question.text = "Contact info?"
        mock_question.weight = 5
        mock_section.questions = [mock_question]
        mock_structure.sections = [mock_section]

        mock_db = MagicMock()

        with patch(
            "app.services.report_generator.AICacheService"
        ) as mock_cache_service:
            mock_cache_instance = MagicMock()
            mock_cache_instance.get_cached_artifact.return_value = None
            mock_cache_instance.compute_answers_hash.return_value = "hash123"
            mock_cache_service.return_value = mock_cache_instance

            with patch(
                "app.services.report_generator.benchmark_context_service"
            ) as mock_benchmark:
                mock_benchmark.get_relevant_context.return_value = []

                with patch(
                    "app.services.report_generator.build_section_prompt_v2"
                ) as mock_build_prompt:
                    mock_build_prompt.return_value = ("test prompt", 0)

                    with patch(
                        "app.services.report_generator.safe_validate_section_artifact"
                    ) as mock_validate:
                        mock_artifact = MagicMock()
                        mock_artifact.model_dump.return_value = {"summary": "test"}
                        mock_validate.return_value = mock_artifact

                        generate_ai_insights(
                            [response_with_pii],
                            mock_structure,
                            mock_key_manager_instance,
                            "report1",
                            mock_db,
                        )

        mock_metrics.increment_pii_redactions.assert_called_once()
        call_args = mock_metrics.increment_pii_redactions.call_args[0]
        assert call_args[0] > 0
