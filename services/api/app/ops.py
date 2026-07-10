import re
import secrets
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


SECRET_PATTERNS = (
    re.compile(r"(?i)(bearer\s+)[^\s]+"),
    re.compile(r"(?i)(access_token[=:]\s*)[^\s,]+"),
    re.compile(r"(?i)(refresh_token[=:]\s*)[^\s,]+"),
)


def redact_secrets(value: str) -> str:
    for pattern in SECRET_PATTERNS:
        value = pattern.sub(r"\1[REDACTED]", value)
    return value


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("x-request-id") or secrets.token_hex(16)
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response


def deletion_plan(user_id: str) -> dict[str, str]:
    return {"user_id": user_id, "action": "delete_user_cascade", "status": "ready"}

