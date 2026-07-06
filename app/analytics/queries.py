from sqlalchemy import case, func

from app.analytics.models import ToolRun, get_session


def files_processed_per_tool() -> list[dict]:
    session = get_session()
    try:
        rows = (
            session.query(ToolRun.tool_name, func.count(ToolRun.id))
            .group_by(ToolRun.tool_name)
            .order_by(func.count(ToolRun.id).desc())
            .all()
        )
        return [{"tool": tool, "count": count} for tool, count in rows]
    finally:
        session.close()


def storage_saved_bytes() -> dict:
    session = get_session()
    try:
        rows = (
            session.query(ToolRun.input_size_bytes, ToolRun.output_size_bytes)
            .filter(ToolRun.tool_name.like("optimize/compress%"))
            .filter(ToolRun.status == "success")
            .filter(ToolRun.output_size_bytes.isnot(None))
            .all()
        )
        before = sum(row[0] for row in rows)
        after = sum(row[1] for row in rows)
        return {"before_bytes": before, "after_bytes": after, "saved_bytes": max(before - after, 0)}
    finally:
        session.close()


def processing_time_trends() -> list[dict]:
    session = get_session()
    try:
        runs = (
            session.query(ToolRun)
            .filter(ToolRun.finished_at.isnot(None))
            .order_by(ToolRun.started_at)
            .all()
        )
        return [
            {
                "tool": run.tool_name,
                "started_at": run.started_at.isoformat(),
                "duration_ms": (run.finished_at - run.started_at).total_seconds() * 1000,
            }
            for run in runs
        ]
    finally:
        session.close()


def error_rate_per_tool() -> list[dict]:
    session = get_session()
    try:
        rows = (
            session.query(
                ToolRun.tool_name,
                func.count(ToolRun.id),
                func.sum(case((ToolRun.status == "failure", 1), else_=0)),
            )
            .group_by(ToolRun.tool_name)
            .all()
        )
        return [
            {
                "tool": tool,
                "total": total,
                "failures": failures or 0,
                "error_rate": round((failures or 0) / total * 100, 1) if total else 0,
            }
            for tool, total, failures in rows
        ]
    finally:
        session.close()


def most_used_tools(limit: int = 5) -> list[dict]:
    return files_processed_per_tool()[:limit]
