from fastapi.testclient import TestClient

from app.core.libreoffice import find_soffice
from app.main import app

client = TestClient(app)


def test_jpg_endpoint(make_image):
    image_path = make_image("photo.jpg")
    files = [("files", ("photo.jpg", image_path.read_bytes(), "image/jpeg"))]
    response = client.post("/api/convert-to-pdf/jpg", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_word_endpoint_without_libreoffice(tmp_path):
    if find_soffice() is not None:
        return
    fake_docx = tmp_path / "doc.docx"
    fake_docx.write_bytes(b"not a real docx")
    response = client.post(
        "/api/convert-to-pdf/word",
        files={
            "file": (
                "doc.docx",
                fake_docx.read_bytes(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )
    assert response.status_code == 503
