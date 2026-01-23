import logging
import time
from collections.abc import Callable

import sentry_sdk
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

SLOW_REQUEST_THRESHOLD = 500
VERY_SLOW_REQUEST_THRESHOLD = 1000


class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        path = request.url.path
        method = request.method
        transaction_name = f"{method} {path}"

        with sentry_sdk.start_transaction(op="http.server", name=transaction_name):
            response: Response = await call_next(request)

            duration_ms = (time.time() - start_time) * 1000

            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

            if duration_ms > VERY_SLOW_REQUEST_THRESHOLD:
                logger.warning(
                    f"Very slow request: {transaction_name} took {duration_ms:.2f}ms"
                )
                sentry_sdk.capture_message(
                    f"Very slow request: {transaction_name} took {duration_ms:.2f}ms",
                    level="warning",
                )
            elif duration_ms > SLOW_REQUEST_THRESHOLD:
                logger.info(
                    f"Slow request: {transaction_name} took {duration_ms:.2f}ms"
                )

            return response
