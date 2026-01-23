import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api import admin, assessment, auth, health, intake, openai_keys, reports
from app.core.config import settings
from app.middleware.csrf import CSRFMiddleware
from app.middleware.performance import PerformanceMiddleware
from app.middleware.rate_limit import limiter
from app.middleware.security_headers import SecurityHeadersMiddleware

logger = logging.getLogger(__name__)


def scrub_pii_from_sentry_event(event: dict, hint: dict | None = None) -> dict | None:
    """Scrub PII from Sentry events before sending"""
    import re

    pii_patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "ip": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    }

    def scrub_string(text: str) -> str:
        """Scrub PII from a string"""
        if not isinstance(text, str):
            return text
        for pii_type, pattern in pii_patterns.items():
            text = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", text)
        return text

    def scrub_dict(data: dict) -> dict:
        """Recursively scrub PII from dictionary"""
        scrubbed = {}
        for key, value in data.items():
            if isinstance(value, str):
                scrubbed[key] = scrub_string(value)
            elif isinstance(value, dict):
                scrubbed[key] = scrub_dict(value)  # type: ignore[assignment]
            elif isinstance(value, list):
                scrubbed[key] = [  # type: ignore[assignment]
                    scrub_dict(item)
                    if isinstance(item, dict)
                    else scrub_string(item)
                    if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                scrubbed[key] = value
        return scrubbed

    return scrub_dict(event)


if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=settings.SENTRY_PROFILES_SAMPLE_RATE,
        enable_tracing=True,
        send_default_pii=False,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
        before_send=lambda event, hint: scrub_pii_from_sentry_event(event),  # type: ignore[arg-type,return-value]
    )
    logger.info("Sentry performance monitoring initialized with PII scrubbing")
else:
    logger.warning("Sentry DSN not configured, performance monitoring disabled")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting application startup...")

    import os

    try:
        os.makedirs(settings.REPORTS_DIR, exist_ok=True)
        logger.info(f"Reports directory ensured at: {settings.REPORTS_DIR}")
    except Exception as e:
        logger.error(f"Failed to create reports directory: {e}")

    logger.info("Starting cache warming...")
    try:
        from app.services.question_parser import load_assessment_structure_cached

        load_assessment_structure_cached()
        logger.info("Cache warming completed")
    except Exception as e:
        logger.error(f"Cache warming failed: {e}")

    yield


app = FastAPI(
    title="Security Posture Assessment API",
    description="API for comprehensive security posture assessment tool",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
    ],
)

app.add_middleware(CSRFMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(PerformanceMiddleware)

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(assessment.router, prefix="/api/assessment", tags=["assessment"])
app.include_router(intake.router, prefix="/api/intake", tags=["intake"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(openai_keys.router, prefix="/api/admin/openai-keys", tags=["admin"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(health.router, tags=["health"])


@limiter.exempt
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Security Posture Assessment API", "version": "1.0.0"}
