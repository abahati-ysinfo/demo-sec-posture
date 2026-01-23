"""Tests for assessment tier functionality"""

from typing import Any

import pytest

from app.core.assessment_tiers import (
    ASSESSMENT_TIERS,
    get_tier_info,
    get_tier_sections,
)


class TestAssessmentTiers:
    """Test tier definitions and helper functions"""

    def test_all_tiers_defined(self) -> None:
        """Test that all expected tiers are defined"""
        assert "quick" in ASSESSMENT_TIERS
        assert "standard" in ASSESSMENT_TIERS
        assert "deep" in ASSESSMENT_TIERS

    def test_quick_tier_structure(self) -> None:
        """Test Quick tier has correct structure"""
        quick = ASSESSMENT_TIERS["quick"]
        assert quick["name"] == "Quick Check"
        assert "description" in quick
        assert "duration" in quick
        assert "sections" in quick
        assert "total_questions" in quick
        assert isinstance(quick["sections"], list)
        assert len(quick["sections"]) == 3

    def test_standard_tier_structure(self) -> None:
        """Test Standard tier has correct structure"""
        standard = ASSESSMENT_TIERS["standard"]
        assert standard["name"] == "Standard Assessment"
        assert "description" in standard
        assert "duration" in standard
        assert "sections" in standard
        assert "total_questions" in standard
        assert isinstance(standard["sections"], list)
        assert len(standard["sections"]) == 10

    def test_deep_tier_structure(self) -> None:
        """Test Deep tier has correct structure"""
        deep = ASSESSMENT_TIERS["deep"]
        assert deep["name"] == "Deep Dive Assessment"
        assert "description" in deep
        assert "duration" in deep
        assert deep["sections"] == "all"
        assert "total_questions" in deep

    def test_get_tier_sections_quick(self) -> None:
        """Test getting sections for Quick tier"""
        sections = get_tier_sections("quick")
        assert isinstance(sections, list)
        assert len(sections) == 3
        assert "section_1" in sections
        assert "section_4" in sections
        assert "section_10" in sections

    def test_get_tier_sections_standard(self) -> None:
        """Test getting sections for Standard tier"""
        sections = get_tier_sections("standard")
        assert isinstance(sections, list)
        assert len(sections) == 10
        assert "section_1" in sections
        assert "section_4" in sections

    def test_get_tier_sections_deep(self) -> None:
        """Test getting sections for Deep tier returns all sections"""
        sections = get_tier_sections("deep")
        assert isinstance(sections, list)
        assert len(sections) == 19

    def test_get_tier_sections_invalid_tier(self) -> None:
        """Test that invalid tier raises ValueError"""
        with pytest.raises(ValueError, match="Unknown tier"):
            get_tier_sections("invalid_tier")

    def test_get_tier_info_quick(self) -> None:
        """Test getting tier info for Quick tier"""
        info = get_tier_info("quick")
        assert info["name"] == "Quick Check"
        assert "description" in info
        assert "duration" in info
        assert "total_questions" in info

    def test_get_tier_info_standard(self) -> None:
        """Test getting tier info for Standard tier"""
        info = get_tier_info("standard")
        assert info["name"] == "Standard Assessment"
        assert "description" in info
        assert "duration" in info
        assert "total_questions" in info

    def test_get_tier_info_deep(self) -> None:
        """Test getting tier info for Deep tier"""
        info = get_tier_info("deep")
        assert info["name"] == "Deep Dive Assessment"
        assert "description" in info
        assert "duration" in info
        assert "total_questions" in info

    def test_get_tier_info_invalid_tier(self) -> None:
        """Test that invalid tier raises ValueError"""
        with pytest.raises(ValueError, match="Unknown tier"):
            get_tier_info("invalid_tier")


class TestTierEndpoints:
    """Test tier-related API endpoints"""

    def test_get_tiers_endpoint(self, client: Any, auth_token: str) -> None:
        """Test GET /api/assessment/tiers endpoint"""
        response = client.get(
            "/api/assessment/tiers", headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "tiers" in data
        assert "quick" in data["tiers"]
        assert "standard" in data["tiers"]
        assert "deep" in data["tiers"]

        quick = data["tiers"]["quick"]
        assert quick["name"] == "Quick Check"
        assert "description" in quick
        assert "duration" in quick
        assert "total_questions" in quick

    def test_start_with_tier_quick(self, client: Any, auth_token: str) -> None:
        """Test starting assessment with Quick tier"""
        response = client.post(
            "/api/assessment/start-with-tier",
            json={"tier": "quick"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assessment = data["data"]
        assert assessment["status"] == "in_progress"
        assert "selected_section_ids" in assessment
        assert len(assessment["selected_section_ids"]) == 3
        assert assessment["metadata"]["tier"] == "quick"

    def test_start_with_tier_standard(self, client: Any, auth_token: str) -> None:
        """Test starting assessment with Standard tier"""
        response = client.post(
            "/api/assessment/start-with-tier",
            json={"tier": "standard"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assessment = data["data"]
        assert assessment["status"] == "in_progress"
        assert "selected_section_ids" in assessment
        assert len(assessment["selected_section_ids"]) == 10
        assert assessment["metadata"]["tier"] == "standard"

    def test_start_with_tier_deep(self, client: Any, auth_token: str) -> None:
        """Test starting assessment with Deep tier"""
        response = client.post(
            "/api/assessment/start-with-tier",
            json={"tier": "deep"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assessment = data["data"]
        assert assessment["status"] == "in_progress"
        assert "selected_section_ids" in assessment
        assert len(assessment["selected_section_ids"]) == 19
        assert assessment["metadata"]["tier"] == "deep"

    def test_start_with_tier_invalid(self, client: Any, auth_token: str) -> None:
        """Test starting assessment with invalid tier"""
        response = client.post(
            "/api/assessment/start-with-tier",
            json={"tier": "invalid_tier"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Invalid tier" in data["detail"]

    def test_start_with_tier_unauthenticated(self, client: Any) -> None:
        """Test starting assessment with tier without authentication"""
        response = client.post(
            "/api/assessment/start-with-tier",
            json={"tier": "quick"},
        )
        assert response.status_code == 403
