"""Tests for enhanced context extractor service"""

import os
from unittest.mock import Mock

import pytest

from app.services.enhanced_context_extractor import (
    EnhancedContextExtractor,
    get_enhanced_context_extractor,
)


@pytest.fixture
def extractor() -> EnhancedContextExtractor:
    """Create an extractor instance with actual markdown file"""
    current_dir = os.path.dirname(os.path.dirname(__file__))
    md_file_path = os.path.join(current_dir, "data", "security_assessment_questions.md")
    return EnhancedContextExtractor(md_file_path)


class TestEnhancedContextExtractor:
    """Test suite for EnhancedContextExtractor"""

    def test_init(self, extractor: EnhancedContextExtractor) -> None:
        """Test extractor initialization"""
        assert extractor.markdown_file_path is not None
        assert extractor._raw_blocks_cache is None

    def test_load_raw_blocks_caching(self, extractor: EnhancedContextExtractor) -> None:
        """Test that raw blocks are cached after first load"""
        blocks1 = extractor._load_raw_blocks()
        assert extractor._raw_blocks_cache is not None
        assert len(blocks1) > 0

        blocks2 = extractor._load_raw_blocks()
        assert blocks1 is blocks2  # Same object reference

    def test_load_raw_blocks_content(self, extractor: EnhancedContextExtractor) -> None:
        """Test that raw blocks are correctly parsed"""
        blocks = extractor._load_raw_blocks()

        assert "1.1.2_option_quarterly" in blocks
        assert "1.1.2_option_annually" in blocks
        assert "1.1.2_option_only_after_changes" in blocks

        option1_content = blocks["1.1.2_option_quarterly"]
        assert "What This Option Means" in option1_content
        assert "Market Context" in option1_content

    def test_get_option_ordinal_with_question_options(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test option value to ordinal mapping with question options"""
        mock_options = [
            Mock(value="annually"),
            Mock(value="bi-annually"),
            Mock(value="as-needed"),
            Mock(value="never"),
        ]

        assert extractor._get_option_ordinal("annually", mock_options) == "1"
        assert extractor._get_option_ordinal("bi-annually", mock_options) == "2"
        assert extractor._get_option_ordinal("as-needed", mock_options) == "3"
        assert extractor._get_option_ordinal("never", mock_options) == "4"

    def test_get_option_ordinal_without_question_options(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test option value to ordinal mapping without question options"""
        assert extractor._get_option_ordinal("1", None) == "1"
        assert extractor._get_option_ordinal("2", None) == "2"
        assert extractor._get_option_ordinal("annually", None) == "annually"

    def test_get_option_ordinal_no_match(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test option value to ordinal mapping with no match"""
        mock_options = [Mock(value="yes"), Mock(value="no")]

        assert extractor._get_option_ordinal("maybe", mock_options) == "maybe"

    def test_get_enhanced_context_with_content(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test getting enhanced context for option with enhanced content"""
        context = extractor.get_enhanced_context("1.1.2", "quarterly")

        assert len(context) > 0
        assert "what_this_means" in context or "market_context" in context

    def test_get_enhanced_context_nonexistent_option(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test getting enhanced context for nonexistent option"""
        context = extractor.get_enhanced_context("999.999.999", "1")

        assert context == {}

    def test_get_enhanced_context_with_underscore_id(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test that question IDs with underscores are normalized"""
        context1 = extractor.get_enhanced_context("1_1_2", "1")
        context2 = extractor.get_enhanced_context("1.1.2", "1")

        assert context1 == context2

    def test_get_enhanced_context_with_question_options(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test getting enhanced context with question options mapping"""
        mock_options = [
            Mock(value="annually"),
            Mock(value="bi-annually"),
        ]

        context = extractor.get_enhanced_context("1.1.2", "annually", mock_options)

        context_direct = extractor.get_enhanced_context("1.1.2", "1")
        assert context == context_direct

    def test_get_compact_context_with_content(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test getting compact context for option with enhanced content"""
        compact = extractor.get_compact_context("1.1.2", "1", max_chars=400)

        assert isinstance(compact, str)

    def test_get_compact_context_truncated(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test getting compact context with truncation"""
        compact = extractor.get_compact_context("1.1.2", "1", max_chars=50)

        assert len(compact) <= 50

    def test_get_compact_context_no_enhanced_content(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test getting compact context for option without enhanced content"""
        compact = extractor.get_compact_context("999.999.999", "1", max_chars=400)

        assert compact == ""

    def test_get_compact_context_with_question_options(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test getting compact context with question options mapping"""
        mock_options = [Mock(value="annually")]

        compact = extractor.get_compact_context(
            "1.1.2", "annually", max_chars=400, question_options=mock_options
        )

        compact_direct = extractor.get_compact_context("1.1.2", "1", max_chars=400)
        assert compact == compact_direct

    def test_has_enhanced_content_with_content(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test has_enhanced_content for option with content"""
        result = extractor.has_enhanced_content("1.1.2", "1")
        assert isinstance(result, bool)

    def test_has_enhanced_content_nonexistent(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test has_enhanced_content returns False for nonexistent option"""
        assert extractor.has_enhanced_content("999.999.999", "1") is False

    def test_extract_section(self, extractor: EnhancedContextExtractor) -> None:
        """Test extracting a section from content"""
        content = """**📋 What This Option Means:**
- **Definition:** This is a test definition.
- **Why It Matters:** This is why it matters.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 50% of organizations
"""

        result = extractor._extract_section(
            content, r"(?:📋\s*)?What This Option Means"
        )

        assert "Definition" in result
        assert "Why It Matters" in result
        assert "Market Context" not in result  # Should stop at next section

    def test_extract_section_not_found(
        self, extractor: EnhancedContextExtractor
    ) -> None:
        """Test extracting section that doesn't exist"""
        content = "Some basic content without sections."

        result = extractor._extract_section(
            content, r"(?:📋\s*)?What This Option Means"
        )

        assert result == ""


class TestGetEnhancedContextExtractor:
    """Test suite for get_enhanced_context_extractor singleton function"""

    def test_singleton_instance(self) -> None:
        """Test that get_enhanced_context_extractor returns singleton"""
        import app.services.enhanced_context_extractor as module

        module._extractor_instance = None

        extractor1 = get_enhanced_context_extractor()
        assert extractor1 is not None

        extractor2 = get_enhanced_context_extractor()
        assert extractor1 is extractor2

    def test_singleton_uses_correct_path(self) -> None:
        """Test that singleton uses correct markdown file path"""
        import app.services.enhanced_context_extractor as module

        module._extractor_instance = None

        extractor = get_enhanced_context_extractor()

        assert "security_assessment_questions.md" in extractor.markdown_file_path
        assert os.path.exists(extractor.markdown_file_path)
