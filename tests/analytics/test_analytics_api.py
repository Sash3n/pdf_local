from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_summary_endpoint_records_organize_run(make_pdf):
    data = make_pdf("source.pdf", pages=2).read_bytes()
    files = [("files", ("source.pdf", data, "application/pdf"))]
    merge_response = client.post("/api/organize/merge", files=files)
    assert merge_response.status_code == 200

    summary_response = client.get("/api/analytics/summary")
    assert summary_response.status_code == 200
    body = summary_response.json()
    tool_names = [row["tool"] for row in body["files_processed_per_tool"]]
    assert "organize/merge" in tool_names


def test_dashboard_page_renders():
    response = client.get("/analytics")
    assert response.status_code == 200
    assert "Analytics" in response.text
