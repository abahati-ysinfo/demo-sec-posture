"""Tests for AI services: prompt_builder, benchmark_context, and ai_cache"""

from typing import Any

import pytest
from pydantic import ValidationError

from app.schemas.ai_artifacts import (
    Benchmark,
    Gap,
    Recommendation,
    SectionAIArtifact,
)
from app.services.ai_cache import AICacheService
from app.services.benchmark_context import BenchmarkContextService
from app.services.prompt_builder import build_section_prompt_v2


class MockSection:
    """Mock section object for testing"""

    def __init__(self, title: str, description: str, id: str = "test-section"):
        self.title = title
        self.description = description
        self.id = id


class TestPromptBuilder:
    """Tests for prompt_builder service"""

    def test_build_section_prompt_basic(self) -> None:
        """Test basic prompt building without curated context"""
        section = MockSection(
            title="Access Control",
            description="Test access control policies",
        )
        section_responses = [
            {"answer": "Yes", "weight": 1.0, "question": "Do you use MFA?"},
            {"answer": "No", "weight": 0.8, "question": "Do you have RBAC?"},
        ]

        prompt, redaction_count = build_section_prompt_v2(section, section_responses)

        assert "Access Control" in prompt
        assert "Test access control policies" in prompt
        assert "Q1: Yes (weight:1.0)" in prompt
        assert "Q2: No (weight:0.8)" in prompt
        assert "risk_level" in prompt
        assert "STRICT REQUIREMENTS" in prompt
        assert redaction_count == 0

    def test_build_section_prompt_with_curated_context(self) -> None:
        """Test prompt building with curated benchmark context"""
        section = MockSection(
            title="Authentication",
            description="Authentication policies",
        )
        section_responses = [
            {"answer": "Partial", "weight": 0.9, "question": "MFA enabled?"}
        ]
        curated_context = "\n\nRELEVANT INDUSTRY CONTROLS:\nNIST CSF PR.AC-7: Multi-factor authentication\n"

        prompt, redaction_count = build_section_prompt_v2(
            section, section_responses, curated_context=curated_context
        )

        assert "RELEVANT INDUSTRY CONTROLS" in prompt
        assert "NIST CSF PR.AC-7" in prompt
        assert "Multi-factor authentication" in prompt
        assert redaction_count == 0

    def test_build_section_prompt_empty_responses(self) -> None:
        """Test prompt building with empty responses list"""
        section = MockSection(title="Test", description="Test description")
        section_responses: list[Any] = []

        prompt, redaction_count = build_section_prompt_v2(section, section_responses)

        assert "Test" in prompt
        assert "Signals:" in prompt
        assert "risk_level" in prompt
        assert redaction_count == 0


class TestBenchmarkContextService:
    """Tests for benchmark_context service"""

    def test_get_relevant_context_authentication(self) -> None:
        """Test getting relevant context for authentication-related sections"""
        service = BenchmarkContextService()

        context = service.get_relevant_context(
            section_title="Multi-Factor Authentication",
            section_description="Policies for MFA and authentication",
            max_controls=5,
        )

        assert context != ""
        assert "RELEVANT INDUSTRY CONTROLS" in context

    def test_get_relevant_context_access_control(self) -> None:
        """Test getting relevant context for access control sections"""
        service = BenchmarkContextService()

        context = service.get_relevant_context(
            section_title="Access Control Management",
            section_description="Role-based access control and permissions",
            max_controls=5,
        )

        assert context != ""
        assert "RELEVANT INDUSTRY CONTROLS" in context

    def test_get_relevant_context_no_matches(self) -> None:
        """Test getting context when no keywords match"""
        service = BenchmarkContextService()

        context = service.get_relevant_context(
            section_title="XYZ",
            section_description="abc def",
            max_controls=5,
        )

        assert context == ""

    def test_extract_keywords(self) -> None:
        """Test keyword extraction from text"""
        service = BenchmarkContextService()

        keywords = service._extract_keywords(
            "Multi-Factor Authentication and Access Control"
        )

        assert "multi-factor" in keywords
        assert "authentication" in keywords
        assert "access" in keywords
        assert "control" in keywords
        assert "and" not in keywords  # Too short


class TestAICacheService:
    """Tests for ai_cache service"""

    def test_compute_answers_hash_deterministic(self) -> None:
        """Test that hash computation is deterministic"""
        service = AICacheService()

        section_responses = [
            {"question": "Do you use MFA?", "answer": "Yes", "weight": 1.0},
            {"question": "Do you have RBAC?", "answer": "No", "weight": 0.8},
        ]

        hash1 = service.compute_answers_hash(section_responses)
        hash2 = service.compute_answers_hash(section_responses)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex digest

    def test_compute_answers_hash_order_independent(self) -> None:
        """Test that hash is order-independent"""
        service = AICacheService()

        responses1 = [
            {"question": "Question A", "answer": "Yes", "weight": 1.0},
            {"question": "Question B", "answer": "No", "weight": 0.8},
        ]
        responses2 = [
            {"question": "Question B", "answer": "No", "weight": 0.8},
            {"question": "Question A", "answer": "Yes", "weight": 1.0},
        ]

        hash1 = service.compute_answers_hash(responses1)
        hash2 = service.compute_answers_hash(responses2)

        assert hash1 == hash2

    def test_compute_answers_hash_normalization(self) -> None:
        """Test that hash normalizes whitespace and case"""
        service = AICacheService()

        responses1 = [{"question": "Question A", "answer": "  YES  ", "weight": 1.0}]
        responses2 = [{"question": "Question A", "answer": "yes", "weight": 1.0}]

        hash1 = service.compute_answers_hash(responses1)
        hash2 = service.compute_answers_hash(responses2)

        assert hash1 == hash2

    def test_compute_answers_hash_different_answers(self) -> None:
        """Test that different answers produce different hashes"""
        service = AICacheService()

        responses1 = [{"question": "Question A", "answer": "Yes", "weight": 1.0}]
        responses2 = [{"question": "Question A", "answer": "No", "weight": 1.0}]

        hash1 = service.compute_answers_hash(responses1)
        hash2 = service.compute_answers_hash(responses2)

        assert hash1 != hash2


class TestAIArtifactSchemas:
    """Tests for AI artifact Pydantic schemas and validators"""

    def test_recommendation_requires_linked_signals(self) -> None:
        """Test that recommendations must have linked signals"""
        rec = Recommendation(  # type: ignore[call-arg]
            action="Implement MFA for all accounts",
            rationale="MFA reduces account compromise risk",
            linked_signals=["Q1", "Q7"],
            effort="Medium",
            impact="High",
            timeline="30-day",
        )
        assert rec.linked_signals == ["Q1", "Q7"]

        with pytest.raises(ValidationError):
            Recommendation(  # type: ignore[call-arg]
                action="Implement MFA",
                rationale="Important",
                linked_signals=[],  # Empty list should fail
                effort="Medium",
                impact="High",
                timeline="30-day",
            )

    def test_gap_requires_linked_signals(self) -> None:
        """Test that gaps must have linked signals"""
        gap = Gap(
            gap="No MFA for admin accounts",
            linked_signals=["Q7"],
            severity="High",
        )
        assert gap.linked_signals == ["Q7"]

        with pytest.raises(ValidationError):
            Gap(
                gap="No MFA",
                linked_signals=[],  # Empty list should fail
                severity="High",
            )

    def test_section_artifact_validates_gaps_have_signals(self) -> None:
        """Test that SectionAIArtifact validates gaps have signals"""
        artifact = SectionAIArtifact(  # type: ignore[call-arg]
            risk_level="High",
            risk_explanation="Multiple critical gaps identified in authentication controls",
            strengths=["Strong password policy"],
            gaps=[
                Gap(
                    gap="No MFA for admin accounts",
                    linked_signals=["Q7"],
                    severity="High",
                )
            ],
            recommendations=[
                Recommendation(  # type: ignore[call-arg]
                    action="Implement MFA for all accounts",
                    rationale="Multi-factor authentication reduces the risk of account compromise significantly",
                    linked_signals=["Q7"],
                    effort="Medium",
                    impact="High",
                    timeline="30-day",
                )
            ],
            benchmarks=[
                Benchmark(  # type: ignore[call-arg]
                    control="Multi-Factor Authentication",
                    status="Missing",
                    framework="NIST",
                    reference="PR.AC-7",
                )
            ],
        )
        assert artifact.risk_level == "High"

    def test_section_artifact_validates_recommendations_have_signals(self) -> None:
        """Test that SectionAIArtifact validates recommendations have signals"""
        with pytest.raises(ValidationError):
            SectionAIArtifact(  # type: ignore[call-arg]
                risk_level="Medium",
                risk_explanation="Some gaps identified",
                strengths=["Good policy"],
                gaps=[
                    Gap(
                        gap="Some gap",
                        linked_signals=["Q1"],
                        severity="Medium",
                    )
                ],
                recommendations=[
                    Recommendation(  # type: ignore[call-arg]
                        action="Fix something",
                        rationale="Important",
                        linked_signals=[],  # Empty - should fail
                        effort="Low",
                        impact="Medium",
                        timeline="60-day",
                    )
                ],
                benchmarks=[
                    Benchmark(  # type: ignore[call-arg]
                        control="Test",
                        status="Partial",
                        framework="NIST",
                    )
                ],
            )

    def test_signal_format_validation(self) -> None:
        """Test that signal IDs must start with 'Q'"""
        gap = Gap(
            gap="Test gap for validation purposes",
            linked_signals=["Q1", "Q7", "Q12"],
            severity="Medium",
        )
        assert gap.linked_signals == ["Q1", "Q7", "Q12"]

        with pytest.raises(ValidationError):
            Gap(
                gap="Test gap for validation purposes",
                linked_signals=["1", "7"],  # Missing 'Q' prefix
                severity="Medium",
            )
