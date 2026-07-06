from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime

from app.analytics.models import ToolRun, get_session


class RunTracker:
    def __init__(self, run: ToolRun):
        self._run = run

    def set_output_size(self, size: int) -> None:
        self._run.output_size_bytes = size


@contextmanager
def track_run(
    tool_name: str, input_file_count: int = 1, input_size_bytes: int = 0
) -> Iterator[RunTracker]:
    session = get_session()
    run = ToolRun(
        tool_name=tool_name,
        started_at=datetime.now(UTC),
        input_file_count=input_file_count,
        input_size_bytes=input_size_bytes,
        status="running",
    )
    session.add(run)
    session.commit()
    tracker = RunTracker(run)
    try:
        yield tracker
        run.status = "success"
    except Exception as exc:
        run.status = "failure"
        run.error_message = str(exc)
        raise
    finally:
        run.finished_at = datetime.now(UTC)
        session.commit()
        session.close()
