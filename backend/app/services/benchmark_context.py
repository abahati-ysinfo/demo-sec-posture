"""Benchmark context service for providing curated security control snippets"""

import os
from typing import Any

import yaml  # type: ignore[import-untyped]


class BenchmarkContextService:
    """Provides curated benchmark context for AI prompts"""

    def __init__(self) -> None:
        self.benchmarks = self._load_benchmarks()

    def _load_benchmarks(self) -> dict[str, Any]:
        """Load benchmarks from YAML file"""
        yaml_path = os.path.join(
            os.path.dirname(__file__), "..", "resources", "benchmarks.yaml"
        )
        with open(yaml_path) as f:
            result: dict[str, Any] = yaml.safe_load(f)
            return result

    def get_relevant_context(
        self, section_title: str, section_description: str, max_controls: int = 5
    ) -> str:
        """Get relevant benchmark controls for a section"""

        keywords = self._extract_keywords(section_title + " " + section_description)

        relevant_controls = []

        for _category, controls in self.benchmarks.get("nist_csf", {}).items():
            for control in controls:
                if self._matches_keywords(control["keywords"], keywords):
                    relevant_controls.append(
                        {
                            "framework": "NIST CSF",
                            "id": control["id"],
                            "control": control["control"],
                            "description": control["description"],
                        }
                    )

        for _category, controls in self.benchmarks.get("iso_27001", {}).items():
            for control in controls:
                if self._matches_keywords(control["keywords"], keywords):
                    relevant_controls.append(
                        {
                            "framework": "ISO 27001",
                            "id": control["id"],
                            "control": control["control"],
                            "description": control["description"],
                        }
                    )

        for control in self.benchmarks.get("owasp_top_10", []):
            if self._matches_keywords(control["keywords"], keywords):
                relevant_controls.append(
                    {
                        "framework": "OWASP Top 10",
                        "id": control["id"],
                        "control": control["control"],
                        "description": control["description"],
                    }
                )

        for control in self.benchmarks.get("cis_controls", []):
            if self._matches_keywords(control["keywords"], keywords):
                relevant_controls.append(
                    {
                        "framework": "CIS Controls",
                        "id": control["id"],
                        "control": control["control"],
                        "description": control["description"],
                    }
                )

        relevant_controls = relevant_controls[:max_controls]

        if not relevant_controls:
            return ""

        context = "\n\nRELEVANT INDUSTRY CONTROLS:\n"
        for ctrl in relevant_controls:
            context += f"\n{ctrl['framework']} {ctrl['id']}: {ctrl['control']}\n"
            context += f"  → {ctrl['description']}\n"

        context += "\nUse these controls as benchmarks in your analysis.\n"
        return context

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract keywords from text"""
        return [word.lower() for word in text.split() if len(word) > 3]

    def _matches_keywords(
        self, control_keywords: list[str], text_keywords: list[str]
    ) -> bool:
        """Check if control keywords match text keywords"""
        return any(kw in text_keywords for kw in control_keywords)


benchmark_context_service = BenchmarkContextService()
