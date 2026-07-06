from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_jpg_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=2).read_bytes()
    response = client.post(
        "/api/convert-from-pdf/jpg", files={"file": ("source.pdf", data, "application/pdf")}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"


def test_word_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    response = client.post(
        "/api/convert-from-pdf/word", files={"file": ("source.pdf", data, "application/pdf")}
    )
    assert response.status_code == 200


def test_excel_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    response = client.post(
        "/api/convert-from-pdf/excel", files={"file": ("source.pdf", data, "application/pdf")}
    )
    assert response.status_code == 200
