"""CSRF protection middleware for Phase 1.3"""

import logging
from collections.abc import Callable

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings
from app.core.security import verify_token
from app.services.security_metrics import security_metrics

logger = logging.getLogger(__name__)

CSRF_EXEMPT_PATHS = {
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/logout",
    "/api/auth/csrf",
    "/",
}

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


class CSRFMiddleware(BaseHTTPMiddleware):
    """CSRF protection using JWT-embedded token validation"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.ENABLE_CSRF or not settings.ENABLE_COOKIE_AUTH:
            bypass_response: Response = await call_next(request)
            return bypass_response

        if request.method in SAFE_METHODS:
            safe_response: Response = await call_next(request)
            return safe_response

        if request.url.path in CSRF_EXEMPT_PATHS:
            exempt_response: Response = await call_next(request)
            return exempt_response

        csrf_header = request.headers.get("X-CSRF-Token")
        if not csrf_header:
            security_metrics.increment_csrf_failures()
            logger.warning(
                f"CSRF token missing for {request.method} {request.url.path}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token missing",
            )

        auth_cookie = request.cookies.get("access_token")
        if not auth_cookie:
            security_metrics.increment_csrf_failures()
            logger.warning(
                f"Auth cookie missing for CSRF validation on {request.url.path}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required for CSRF validation",
            )

        try:
            token_data = verify_token(auth_cookie)
            jwt_csrf = token_data.get("csrf", "")

            if not jwt_csrf or csrf_header != jwt_csrf:
                security_metrics.increment_csrf_failures()
                logger.warning(
                    f"CSRF token mismatch for {request.method} {request.url.path}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="CSRF token invalid",
                )
        except HTTPException:
            raise
        except Exception as e:
            security_metrics.increment_csrf_failures()
            logger.error(f"CSRF validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF validation failed",
            )

        response: Response = await call_next(request)
        return response
