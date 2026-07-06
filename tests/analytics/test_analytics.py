from app.analytics.queries import (
    error_rate_per_tool,
    files_processed_per_tool,
    most_used_tools,
    processing_time_trends,
    storage_saved_bytes,
)
from app.analytics.tracker import track_run


def test_track_run_records_success():
    with track_run("organize/merge", input_file_count=2, input_size_bytes=1000) as run:
        run.set_output_size(500)

    rows = files_processed_per_tool()
    assert rows == [{"tool": "organize/merge", "count": 1}]


def test_track_run_records_failure():
    try:
        with track_run("organize/merge"):
            raise ValueError("boom")
    except ValueError:
        pass

    rows = error_rate_per_tool()
    assert rows == [{"tool": "organize/merge", "total": 1, "failures": 1, "error_rate": 100.0}]


def test_storage_saved_bytes_for_compress():
    with track_run("optimize/compress", input_size_bytes=1000) as run:
        run.set_output_size(400)

    saved = storage_saved_bytes()
    assert saved == {"before_bytes": 1000, "after_bytes": 400, "saved_bytes": 600}


def test_processing_time_trends_records_duration():
    with track_run("organize/split"):
        pass

    trends = processing_time_trends()
    assert len(trends) == 1
    assert trends[0]["tool"] == "organize/split"
    assert trends[0]["duration_ms"] >= 0


def test_most_used_tools_orders_by_count():
    with track_run("organize/merge"):
        pass
    with track_run("organize/merge"):
        pass
    with track_run("organize/split"):
        pass

    top = most_used_tools(limit=1)
    assert top == [{"tool": "organize/merge", "count": 2}]
