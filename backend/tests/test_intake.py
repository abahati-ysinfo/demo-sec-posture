"""Tests for intake wizard feature"""

from unittest.mock import MagicMock, patch

from app.schemas.intake import (
    AIRecommendationResponse,
    IntakeAnswers,
    SectionMetadata,
    SectionRecommendation,
    UserProfile,
)
from app.services.intake_prompt_builder import build_messages, get_openai_params
from app.services.intake_service import (
    apply_guardrails,
    call_openai_for_recommendations,
    generate_fallback_recommendations,
    load_sections_metadata,
    map_answers_to_profile,
)


class TestIntakePromptBuilder:
    """Tests for intake prompt builder"""

    def test_get_openai_params(self) -> None:
        """Test OpenAI parameters are correct"""
        params = get_openai_params()

        assert params["model"] == "gpt-4o-mini"
        assert params["temperature"] == 0.2
        assert "response_format" in params

    def test_build_messages_structure(self) -> None:
        """Test that messages include required components"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Finance",
            environment="Hybrid",
            system_types=["public_web_apps"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        sections = [
            SectionMetadata(
                id="section_1",
                name="Governance",
                description="Test",
                tags=["governance"],
            )
        ]

        messages = build_messages(user_profile, sections)

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert "JSON" in messages[0]["content"]
        assert "moderate" in messages[1]["content"]


class TestIntakeServiceMapping:
    """Tests for intake service answer mapping"""

    def test_map_answers_to_profile_basic(self) -> None:
        """Test basic answer to profile mapping"""
        answers = IntakeAnswers(
            role="IT Manager",
            org_size="51-250",
            sector="Finance",
            environment="Hybrid",
            system_types=["public_web_apps"],
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )

        profile = map_answers_to_profile(answers)

        assert profile.role == "IT Manager"
        assert profile.org_size == "51-250"
        assert profile.has_ot_ics is False
        assert profile.time_preference == "moderate"

    def test_map_answers_to_profile_with_ot_ics(self) -> None:
        """Test that OT/ICS flag is set correctly"""
        answers = IntakeAnswers(
            role="Security Manager",
            org_size="251-1000",
            sector="Energy/Utilities",
            environment="Hybrid",
            system_types=["ot_ics", "public_web_apps"],
            cloud_providers=[],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="deep",
        )

        profile = map_answers_to_profile(answers)

        assert profile.has_ot_ics is True


class TestIntakeServiceFallback:
    """Tests for intake service fallback logic"""

    def test_generate_fallback_recommendations_includes_core_sections(self) -> None:
        """Test that fallback always includes core sections"""
        user_profile = UserProfile(
            role="CISO",
            org_size="51-250",
            sector="General Corporate",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_10", name="Incident Response", description="Test", tags=[]
            ),
        ]

        response = generate_fallback_recommendations(user_profile, sections)

        section_ids = [rec.id for rec in response.recommended_sections]
        assert "section_1" in section_ids
        assert "section_4" in section_ids
        assert "section_10" in section_ids

    def test_generate_fallback_recommendations_includes_cloud_for_cloud_users(
        self,
    ) -> None:
        """Test that fallback includes cloud section for cloud users"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Technology",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=["AWS", "Azure"],
            primary_goal="Focus specifically on cloud and identity security",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_9", name="Cloud Security", description="Test", tags=[]
            ),
            SectionMetadata(
                id="section_10", name="Incident Response", description="Test", tags=[]
            ),
        ]

        response = generate_fallback_recommendations(user_profile, sections)

        section_ids = [rec.id for rec in response.recommended_sections]
        assert "section_9" in section_ids

    def test_generate_fallback_recommendations_includes_ot_for_ot_users(self) -> None:
        """Test that fallback includes OT section for OT/ICS users"""
        user_profile = UserProfile(
            role="Security Manager",
            org_size="251-1000",
            sector="Energy/Utilities",
            environment="Hybrid",
            system_types=["ot_ics"],
            has_ot_ics=True,
            cloud_providers=[],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="deep",
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_10", name="Incident Response", description="Test", tags=[]
            ),
            SectionMetadata(
                id="section_18", name="OT/ICS Security", description="Test", tags=[]
            ),
        ]

        response = generate_fallback_recommendations(user_profile, sections)

        section_ids = [rec.id for rec in response.recommended_sections]
        assert "section_18" in section_ids

    def test_generate_fallback_recommendations_excludes_ot_for_non_ot_users(
        self,
    ) -> None:
        """Test that fallback excludes OT section for non-OT users"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Technology",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_18", name="OT/ICS Security", description="Test", tags=[]
            ),
        ]

        response = generate_fallback_recommendations(user_profile, sections)

        excluded_ids = [exc.id for exc in response.excluded_sections]
        assert "section_18" in excluded_ids

    def test_generate_fallback_recommendations_respects_quick_time_cap(self) -> None:
        """Test that fallback respects quick time preference cap"""
        user_profile = UserProfile(
            role="CISO",
            org_size="51-250",
            sector="General Corporate",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="quick",
        )
        sections = [
            SectionMetadata(
                id=f"section_{i}",
                name=f"Section {i}",
                description="Test",
                tags=[],
            )
            for i in range(1, 20)
        ]

        response = generate_fallback_recommendations(user_profile, sections)

        assert len(response.recommended_sections) <= 5


class TestIntakeServiceGuardrails:
    """Tests for intake service guardrails"""

    def test_apply_guardrails_adds_iam_if_missing(self) -> None:
        """Test that guardrails always add IAM if missing"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Technology",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        ai_response = AIRecommendationResponse(
            recommended_sections=[
                SectionRecommendation(
                    id="section_1", priority="must_do", reason="Test", confidence=0.9
                )
            ],
            excluded_sections=[],
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
        ]

        result = apply_guardrails(ai_response, user_profile, sections)

        section_ids = [rec.id for rec in result.recommended_sections]
        assert "section_4" in section_ids

    def test_apply_guardrails_adds_cloud_for_cloud_users(self) -> None:
        """Test that guardrails add cloud section for cloud users"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Technology",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        ai_response = AIRecommendationResponse(
            recommended_sections=[
                SectionRecommendation(
                    id="section_1", priority="must_do", reason="Test", confidence=0.9
                )
            ],
            excluded_sections=[],
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_9", name="Cloud Security", description="Test", tags=[]
            ),
        ]

        result = apply_guardrails(ai_response, user_profile, sections)

        section_ids = [rec.id for rec in result.recommended_sections]
        assert "section_9" in section_ids
        assert "section_4" in section_ids

    def test_apply_guardrails_adds_ot_for_ot_users(self) -> None:
        """Test that guardrails add OT section for OT/ICS users"""
        user_profile = UserProfile(
            role="Security Manager",
            org_size="251-1000",
            sector="Energy/Utilities",
            environment="Hybrid",
            system_types=["ot_ics"],
            has_ot_ics=True,
            cloud_providers=[],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        ai_response = AIRecommendationResponse(
            recommended_sections=[
                SectionRecommendation(
                    id="section_1", priority="must_do", reason="Test", confidence=0.9
                )
            ],
            excluded_sections=[],
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_18", name="OT/ICS Security", description="Test", tags=[]
            ),
        ]

        result = apply_guardrails(ai_response, user_profile, sections)

        section_ids = [rec.id for rec in result.recommended_sections]
        assert "section_18" in section_ids

    def test_apply_guardrails_respects_quick_time_cap(self) -> None:
        """Test that guardrails respect quick time preference cap"""
        user_profile = UserProfile(
            role="CISO",
            org_size="51-250",
            sector="General Corporate",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=[],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="quick",
        )
        ai_response = AIRecommendationResponse(
            recommended_sections=[
                SectionRecommendation(
                    id=f"section_{i}",
                    priority="must_do" if i < 4 else "should_do",
                    reason="Test",
                    confidence=0.9,
                )
                for i in range(1, 11)
            ],
            excluded_sections=[],
        )
        sections = [
            SectionMetadata(
                id=f"section_{i}",
                name=f"Section {i}",
                description="Test",
                tags=[],
            )
            for i in range(1, 11)
        ]

        result = apply_guardrails(ai_response, user_profile, sections)

        assert len(result.recommended_sections) <= 5

    def test_apply_guardrails_respects_moderate_time_cap(self) -> None:
        """Test that guardrails respect moderate time preference cap"""
        user_profile = UserProfile(
            role="CISO",
            org_size="51-250",
            sector="General Corporate",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=[],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        ai_response = AIRecommendationResponse(
            recommended_sections=[
                SectionRecommendation(
                    id=f"section_{i}",
                    priority="must_do" if i < 5 else "should_do",
                    reason="Test",
                    confidence=0.9,
                )
                for i in range(1, 15)
            ],
            excluded_sections=[],
        )
        sections = [
            SectionMetadata(
                id=f"section_{i}",
                name=f"Section {i}",
                description="Test",
                tags=[],
            )
            for i in range(1, 15)
        ]

        result = apply_guardrails(ai_response, user_profile, sections)

        assert len(result.recommended_sections) <= 8

    def test_apply_guardrails_filters_invalid_section_ids(self) -> None:
        """Test that guardrails filter out invalid section IDs"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Technology",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=[],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        ai_response = AIRecommendationResponse(
            recommended_sections=[
                SectionRecommendation(
                    id="section_1", priority="must_do", reason="Test", confidence=0.9
                ),
                SectionRecommendation(
                    id="invalid_section",
                    priority="must_do",
                    reason="Test",
                    confidence=0.9,
                ),
            ],
            excluded_sections=[],
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
        ]

        result = apply_guardrails(ai_response, user_profile, sections)

        section_ids = [rec.id for rec in result.recommended_sections]
        assert "section_1" in section_ids
        assert "invalid_section" not in section_ids

    def test_generate_fallback_recommendations_includes_app_security(self) -> None:
        """Test that fallback includes app security for web/custom apps"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Technology",
            environment="Mostly in the cloud",
            system_types=["public_web_apps", "internal_custom_apps"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_8", name="Application Security", description="Test", tags=[]
            ),
            SectionMetadata(
                id="section_10", name="Incident Response", description="Test", tags=[]
            ),
        ]

        response = generate_fallback_recommendations(user_profile, sections)

        section_ids = [rec.id for rec in response.recommended_sections]
        assert "section_8" in section_ids

    def test_generate_fallback_recommendations_includes_risk_mgmt_for_posture_goal(
        self,
    ) -> None:
        """Test that fallback includes risk management for overall posture goal"""
        user_profile = UserProfile(
            role="CISO",
            org_size="51-250",
            sector="General Corporate",
            environment="Mostly in the cloud",
            system_types=["saas"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(
                id="section_2", name="Risk Management", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
            SectionMetadata(
                id="section_10", name="Incident Response", description="Test", tags=[]
            ),
        ]

        response = generate_fallback_recommendations(user_profile, sections)

        section_ids = [rec.id for rec in response.recommended_sections]
        assert "section_2" in section_ids


class TestIntakeServiceHelpers:
    """Tests for intake service helper functions"""

    def test_load_sections_metadata(self) -> None:
        """Test that sections metadata loads successfully"""
        sections = load_sections_metadata()

        assert len(sections) > 0
        assert all(isinstance(s, SectionMetadata) for s in sections)
        assert all(s.id and s.name and s.description for s in sections)

    def test_call_openai_for_recommendations_success(self) -> None:
        """Test successful OpenAI call for recommendations"""
        user_profile = UserProfile(
            role="IT Manager",
            org_size="51-250",
            sector="Finance",
            environment="Hybrid",
            system_types=["public_web_apps"],
            has_ot_ics=False,
            cloud_providers=["AWS"],
            primary_goal="Understand our overall security posture",
            primary_goal_detail=None,
            time_preference="moderate",
        )
        sections = [
            SectionMetadata(
                id="section_1", name="Governance", description="Test", tags=[]
            ),
            SectionMetadata(id="section_4", name="IAM", description="Test", tags=[]),
        ]

        mock_key_manager = MagicMock()
        mock_key_manager.get_next_key.return_value = ("key_id", "test_api_key")

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = '{"recommended_sections": [{"id": "section_1", "priority": "must_do", "reason": "Test", "confidence": 0.9}], "excluded_sections": []}'

        with patch("app.services.intake_service.openai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client

            result, raw = call_openai_for_recommendations(
                user_profile, sections, mock_key_manager
            )

        assert result is not None
        assert isinstance(result, AIRecommendationResponse)
        assert len(result.recommended_sections) == 1
        assert result.recommended_sections[0].id == "section_1"
        mock_key_manager.record_success.assert_called_once_with("key_id")
