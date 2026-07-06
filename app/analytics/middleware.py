from datetime import UTC, datetime

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.analytics.models import ToolRun, get_session

_EXCLUDED_PREFIXES = ("/api/analytics",)


def _tool_name_from_path(path: str) -> str:
    return path.removeprefix("/api/")


class AnalyticsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method != "POST" or not request.url.path.startswith("/api/"):
            return await call_next(request)
        if request.url.path.startswith(_EXCLUDED_PREFIXES):
            return await call_next(request)

        started_at = datetime.now(UTC)
        input_size = int(request.headers.get("content-length") or 0)
        status = "success"
        error_message = None
        response = None
        try:
            response = await call_next(request)
            if response.status_code >= 400:
                status = "failure"
                error_message = f"HTTP {response.status_code}"
            return response
        except Exception as exc:
            status = "failure"
            error_message = str(exc)
            raise
        finally:
            output_size = None
            if response is not None:
                content_length = response.headers.get("content-length")
                output_size = int(content_length) if content_length else None
            session = get_session()
            session.add(
                ToolRun(
                    tool_name=_tool_name_from_path(request.url.path),
                    started_at=started_at,
                    finished_at=datetime.now(UTC),
                    input_file_count=1,
                    input_size_bytes=input_size,
                    output_size_bytes=output_size,
                    status=status,
                    error_message=error_message,
                )
            )
            session.commit()
            session.close()
