from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pdf_to_markdown_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1, text="Hello Markdown").read_bytes()
    response = client.post(
        "/api/intelligence/pdf-to-markdown",
        files={"file": ("source.pdf", data, "application/pdf")},
    )
    assert response.status_code == 200
    assert "Hello Markdown" in response.text
