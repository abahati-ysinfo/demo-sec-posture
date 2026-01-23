"""Enhanced Context Extractor for parsing multi-section option content from markdown"""

import re


class EnhancedContextExtractor:
    """Extract enhanced multi-section content for options from markdown"""

    SECTION_PATTERNS = {
        "what_this_means": r"(?:📋\s*)?What This Option Means",
        "why_it_matters": r"(?:📊\s*)?Why It Matters",
        "market_context": r"(?:📊\s*)?Market Context(?:\s*&\s*Benchmarks)?",
        "compliance": r"(?:⚖️\s*)?Compliance(?:\s*Frameworks?)?",
        "recommendations": r"(?:🎯\s*)?Recommendations(?:\s*&\s*Next Steps)?",
        "path_to_improvement": r"(?:🔄\s*)?Path to Improvement",
    }

    def __init__(self, markdown_file_path: str):
        """Initialize with path to markdown file"""
        self.markdown_file_path = markdown_file_path
        self._raw_blocks_cache = None

    def _load_raw_blocks(self) -> dict[str, str]:
        """Load and cache raw option blocks from markdown"""
        if self._raw_blocks_cache is not None:
            return self._raw_blocks_cache

        raw_blocks = {}

        with open(self.markdown_file_path, encoding="utf-8") as f:
            lines = f.readlines()

        current_question_id = None
        current_option_num = None
        collecting_option_block = False
        option_block_lines = []

        for line in lines:
            question_match = re.match(r"#### Question ([\d.]+)", line)
            if question_match:
                current_question_id = question_match.group(1)
                collecting_option_block = False
                continue

            option_match = re.match(r"\*\*Option ([a-z0-9_]+):", line)
            if option_match and current_question_id:
                if collecting_option_block and current_option_num:
                    key = f"{current_question_id}_option_{current_option_num}"
                    raw_blocks[key] = "".join(option_block_lines)

                current_option_num = option_match.group(1)
                option_block_lines = [line]
                collecting_option_block = True
                continue

            if collecting_option_block:
                if (
                    line.startswith("####")
                    or line.startswith("###")
                    or line.startswith("##")
                ):
                    key = f"{current_question_id}_option_{current_option_num}"
                    raw_blocks[key] = "".join(option_block_lines)
                    collecting_option_block = False
                    option_block_lines = []
                else:
                    option_block_lines.append(line)

        if collecting_option_block and current_option_num and current_question_id:
            key = f"{current_question_id}_option_{current_option_num}"
            raw_blocks[key] = "".join(option_block_lines)

        self._raw_blocks_cache = raw_blocks  # type: ignore[assignment]
        return raw_blocks

    def _get_option_ordinal(
        self,
        option_value: str,
        question_options: list | None = None,  # type: ignore[assignment]
    ) -> str:
        """Map option value to ordinal number for markdown lookup"""
        if question_options:
            for idx, opt in enumerate(question_options, 1):
                if hasattr(opt, "value") and str(opt.value) == str(option_value):
                    return str(idx)
        return str(option_value)

    def get_enhanced_context(
        self,
        question_id: str,
        option_value: str,
        question_options: list | None = None,  # type: ignore[assignment]
    ) -> dict[str, str]:
        """
        Get enhanced multi-section content for a specific option.

        Args:
            question_id: Question ID (e.g., "1_1_1" or "1.1.1")
            option_value: Option value (e.g., "yes", "no", "annually")
            question_options: Optional list of QuestionOption objects to map value to ordinal

        Returns:
            Dictionary with keys: what_this_means, why_it_matters, market_context,
            compliance, recommendations, path_to_improvement
            Empty dict if no enhanced content exists
        """
        normalized_qid = question_id.replace("_", ".")
        option_ordinal = self._get_option_ordinal(option_value, question_options)

        key = f"{normalized_qid}_option_{option_ordinal}"
        raw_blocks = self._load_raw_blocks()

        if key not in raw_blocks:
            return {}

        raw_content = raw_blocks[key]

        has_enhanced = any(
            re.search(pattern, raw_content, re.IGNORECASE)
            for pattern in self.SECTION_PATTERNS.values()
        )

        if not has_enhanced:
            return {}

        enhanced_context = {}

        for key_name, pattern in self.SECTION_PATTERNS.items():
            section_content = self._extract_section(raw_content, pattern)
            if section_content:
                enhanced_context[key_name] = section_content

        return enhanced_context

    def _extract_section(self, content: str, heading_pattern: str) -> str:
        """Extract content under a specific heading"""
        heading_match = re.search(
            f"^\\s*\\*\\*{heading_pattern}:?\\*\\*\\s*$",
            content,
            re.MULTILINE | re.IGNORECASE,
        )

        if not heading_match:
            return ""

        start_pos = heading_match.end()

        next_section_patterns = [
            r"^\s*(?:\*\*)?(?:📋|📊|⚖️|🎯|🔄)?\s*(?:What This|Why It|Market Context|Compliance|Recommendations|Path to)",
            r"^\*\*Option [a-z0-9_]+:",
            r"^####",
        ]

        end_pos = len(content)
        for pattern in next_section_patterns:
            next_match = re.search(
                pattern, content[start_pos:], re.MULTILINE | re.IGNORECASE
            )
            if next_match:
                end_pos = start_pos + next_match.start()
                break

        section_text = content[start_pos:end_pos].strip()

        section_text = re.sub(r"^\*+\s*", "", section_text)
        section_text = re.sub(r"\s*\*+$", "", section_text)

        return section_text

    def get_compact_context(
        self,
        question_id: str,
        option_value: str,
        max_chars: int = 400,
        question_options: list | None = None,  # type: ignore[assignment]
    ) -> str:
        """
        Get compact enhanced context suitable for AI prompts.

        Args:
            question_id: Question ID
            option_value: Option value
            max_chars: Maximum characters to return
            question_options: Optional list of QuestionOption objects to map value to ordinal

        Returns:
            Compact string with key context, or empty string if none exists
        """
        enhanced = self.get_enhanced_context(
            question_id, option_value, question_options
        )

        if not enhanced:
            return ""

        parts = []

        if "what_this_means" in enhanced:
            text = enhanced["what_this_means"][:150]
            parts.append(f"What it means: {text}")

        if "market_context" in enhanced:
            text = enhanced["market_context"][:120]
            parts.append(f"Market: {text}")

        if "recommendations" in enhanced:
            text = enhanced["recommendations"][:130]
            parts.append(f"Recs: {text}")

        compact = "; ".join(parts)

        if len(compact) > max_chars:
            compact = compact[: max_chars - 3] + "..."

        return compact

    def has_enhanced_content(self, question_id: str, option_value: str) -> bool:
        """Check if enhanced content exists for this option"""
        context = self.get_enhanced_context(question_id, option_value)
        return len(context) > 0


_extractor_instance = None


def get_enhanced_context_extractor() -> EnhancedContextExtractor:
    """Get singleton instance of enhanced context extractor"""
    global _extractor_instance

    if _extractor_instance is None:
        import os

        current_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        md_file_path = os.path.join(
            current_dir, "data", "security_assessment_questions.md"
        )
        _extractor_instance = EnhancedContextExtractor(md_file_path)

    return _extractor_instance
