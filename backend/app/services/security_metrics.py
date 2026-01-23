"""Security observability metrics for Phase 0-2 remediation"""

import logging

logger = logging.getLogger(__name__)


class SecurityMetrics:
    """Simple counter-based metrics for security features"""

    def __init__(self) -> None:
        self._pii_redactions = 0
        self._cookie_auth_requests = 0
        self._csrf_failures = 0
        self._rate_limit_hits = 0

    def increment_pii_redactions(self, count: int = 1) -> None:
        """Track PII redaction events"""
        self._pii_redactions += count
        logger.info(f"PII redactions: {self._pii_redactions} total (+{count})")

    def increment_cookie_auth(self) -> None:
        """Track cookie-based authentication usage"""
        self._cookie_auth_requests += 1
        if self._cookie_auth_requests % 100 == 0:
            logger.info(f"Cookie auth requests: {self._cookie_auth_requests} total")

    def increment_csrf_failures(self) -> None:
        """Track CSRF validation failures"""
        self._csrf_failures += 1
        logger.warning(f"CSRF failures: {self._csrf_failures} total")

    def increment_rate_limit_hits(self) -> None:
        """Track rate limit triggers"""
        self._rate_limit_hits += 1
        logger.info(f"Rate limit hits: {self._rate_limit_hits} total")

    def get_stats(self) -> dict[str, int]:
        """Get current metrics"""
        return {
            "pii_redactions": self._pii_redactions,
            "cookie_auth_requests": self._cookie_auth_requests,
            "csrf_failures": self._csrf_failures,
            "rate_limit_hits": self._rate_limit_hits,
        }


security_metrics = SecurityMetrics()
