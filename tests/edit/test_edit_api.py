from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rotate_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    response = client.post(
        "/api/edit/rotate",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"angle": "90"},
    )
    assert response.status_code == 200


def test_page_numbers_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=2).read_bytes()
    response = client.post(
        "/api/edit/page-numbers", files={"file": ("source.pdf", data, "application/pdf")}
    )
    assert response.status_code == 200


def test_watermark_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    response = client.post(
        "/api/edit/watermark",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"text": "DRAFT"},
    )
    assert response.status_code == 200


def test_crop_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    response = client.post(
        "/api/edit/crop",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"x0": "0", "y0": "0", "x1": "100", "y1": "100"},
    )
    assert response.status_code == 200


def test_text_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    response = client.post(
        "/api/edit/text",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"page": "1", "content": "Hello", "x": "10", "y": "10"},
    )
    assert response.status_code == 200
