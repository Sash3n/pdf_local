import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _pdf_bytes(make_pdf, name, pages):
    path = make_pdf(name, pages=pages)
    return path.read_bytes()


def test_merge_endpoint(make_pdf):
    files = [
        ("files", ("a.pdf", _pdf_bytes(make_pdf, "a.pdf", 2), "application/pdf")),
        ("files", ("b.pdf", _pdf_bytes(make_pdf, "b.pdf", 1), "application/pdf")),
    ]
    response = client.post("/api/organize/merge", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_split_endpoint(make_pdf):
    data = _pdf_bytes(make_pdf, "source.pdf", 3)
    response = client.post(
        "/api/organize/split", files={"file": ("source.pdf", data, "application/pdf")}
    )
    assert response.status_code == 200
    assert response.json() == {"pages": 3}


def test_remove_endpoint(make_pdf):
    data = _pdf_bytes(make_pdf, "source.pdf", 4)
    response = client.post(
        "/api/organize/remove",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"pages": "2"},
    )
    assert response.status_code == 200


def test_extract_endpoint(make_pdf):
    data = _pdf_bytes(make_pdf, "source.pdf", 4)
    response = client.post(
        "/api/organize/extract",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"pages": "1,2"},
    )
    assert response.status_code == 200


def test_reorder_endpoint(make_pdf):
    data = _pdf_bytes(make_pdf, "source.pdf", 3)
    response = client.post(
        "/api/organize/reorder",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"order": "3,2,1"},
    )
    assert response.status_code == 200


def test_scan_to_pdf_endpoint(make_image):
    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (100, 100), (0, 255, 0)).save(buf, format="JPEG")
    buf.seek(0)
    files = [("files", ("scan.jpg", buf.read(), "image/jpeg"))]
    response = client.post("/api/organize/scan-to-pdf", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
