"""PII Redaction Service for protecting user privacy in AI prompts"""

import re
from typing import Any


class PIIRedactor:
    """Detect and redact personally identifiable information (PII) from text"""

    PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "ip_address": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "url_with_params": r"https?://[^\s]+\?[^\s]+",
    }

    REPLACEMENTS = {
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "ssn": "[SSN_REDACTED]",
        "ip_address": "[IP_REDACTED]",
        "credit_card": "[CARD_REDACTED]",
        "url_with_params": "[URL_REDACTED]",
    }

    WHITELIST = [
        r"example\.com",
        r"test@test\.com",
        r"127\.0\.0\.1",
        r"localhost",
        r"0\.0\.0\.0",
    ]

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.redaction_count = 0

    def redact(self, text: str) -> tuple[str, int]:
        """Redact PII from text and return (redacted_text, count)"""
        if not self.enabled or not text:
            return (text, 0)

        redacted = str(text)
        count = 0

        for pii_type, pattern in self.PATTERNS.items():
            matches = list(re.finditer(pattern, redacted, re.IGNORECASE))
            for match in matches:
                match_str = match.group(0)

                is_whitelisted = any(
                    re.search(wl, match_str, re.IGNORECASE) for wl in self.WHITELIST
                )

                if not is_whitelisted:
                    redacted = redacted.replace(match_str, self.REPLACEMENTS[pii_type])
                    count += 1

        self.redaction_count += count
        return (redacted, count)

    def redact_responses(
        self, responses: list[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], int]:
        """Redact PII from list of question/answer responses

        Redacts PII from answer, comment, and context fields if present
        """
        redacted_responses = []
        total_count = 0

        for resp in responses:
            redacted_resp = {**resp}

            answer_value = resp.get("answer", "")
            redacted_answer, count = self.redact(str(answer_value))
            total_count += count
            redacted_resp["answer"] = redacted_answer

            if "comment" in resp and resp["comment"]:
                redacted_comment, count = self.redact(str(resp["comment"]))
                total_count += count
                redacted_resp["comment"] = redacted_comment

            if "context" in resp and resp["context"]:
                redacted_context, count = self.redact(str(resp["context"]))
                total_count += count
                redacted_resp["context"] = redacted_context

            redacted_responses.append(redacted_resp)

        return (redacted_responses, total_count)

    def get_redaction_summary(self) -> dict[str, Any]:
        """Get summary of redactions performed"""
        return {"total_redactions": self.redaction_count, "enabled": self.enabled}


pii_redactor = PIIRedactor()
