import time
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine

router = APIRouter()

STARTUP_TIME = time.time()


def get_uptime_seconds() -> float:
    """Calculate uptime in seconds since application startup"""
    return time.time() - STARTUP_TIME


def check_database() -> dict[str, str]:
    """Check database connectivity"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "message": "Database connection successful"}
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
        }


def check_redis() -> dict[str, str] | None:
    """Check Redis connectivity if configured"""
    if not settings.REDIS_URL:
        return None

    try:
        import redis

        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        r.ping()
        return {"status": "healthy", "message": "Redis connection successful"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"Redis connection failed: {str(e)}"}


@router.get("/health")
async def health_check() -> JSONResponse:
    """
    Comprehensive health check endpoint.
    Returns 200 if all checks pass, 503 if any check fails.
    """
    uptime = get_uptime_seconds()
    db_health = check_database()
    redis_health = check_redis()

    response_data: dict[str, Any] = {
        "status": "healthy",
        "version": "1.0.0",
        "uptime_seconds": round(uptime, 2),
        "timestamp": datetime.now(UTC).isoformat(),
        "checks": {
            "database": db_health,
        },
    }

    if redis_health is not None:
        response_data["checks"]["redis"] = redis_health

    is_healthy = db_health["status"] == "healthy"
    if redis_health is not None:
        is_healthy = is_healthy and redis_health["status"] == "healthy"

    if not is_healthy:
        response_data["status"] = "unhealthy"
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=response_data
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)


@router.get("/health/live")
async def liveness_probe() -> dict[str, str | float]:
    """
    Liveness probe endpoint for Kubernetes/container orchestration.
    Always returns 200 to indicate the application is running.
    """
    return {
        "status": "alive",
        "version": "1.0.0",
        "uptime_seconds": round(get_uptime_seconds(), 2),
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/health/ready")
async def readiness_probe() -> JSONResponse:
    """
    Readiness probe endpoint for Kubernetes/container orchestration.
    Returns 200 if database is accessible, 503 otherwise.
    """
    db_health = check_database()
    uptime = get_uptime_seconds()

    response_data = {
        "status": "ready" if db_health["status"] == "healthy" else "not_ready",
        "version": "1.0.0",
        "uptime_seconds": round(uptime, 2),
        "timestamp": datetime.now(UTC).isoformat(),
        "checks": {"database": db_health},
    }

    if db_health["status"] != "healthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=response_data
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)
