from fastapi import APIRouter

from app.analytics.queries import (
    error_rate_per_tool,
    files_processed_per_tool,
    most_used_tools,
    processing_time_trends,
    storage_saved_bytes,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary")
def summary():
    return {
        "files_processed_per_tool": files_processed_per_tool(),
        "storage_saved": storage_saved_bytes(),
        "processing_time_trends": processing_time_trends(),
        "error_rate_per_tool": error_rate_per_tool(),
        "most_used_tools": most_used_tools(),
    }
