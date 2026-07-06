import fitz
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_compress_endpoint(tmp_path, make_image):
    image_path = make_image("photo.jpg", size=(400, 400))
    doc = fitz.open()
    page = doc.new_page()
    page.insert_image(fitz.Rect(0, 0, 300, 300), filename=str(image_path))
    source = tmp_path / "with_image.pdf"
    doc.save(source)
    doc.close()

    response = client.post(
        "/api/optimize/compress",
        files={"file": ("with_image.pdf", source.read_bytes(), "application/pdf")},
        data={"quality": "40"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_repair_endpoint(make_pdf):
    source = make_pdf("source.pdf", pages=2)
    response = client.post(
        "/api/optimize/repair",
        files={"file": ("source.pdf", source.read_bytes(), "application/pdf")},
    )
    assert response.status_code == 200
