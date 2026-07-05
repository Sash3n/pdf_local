from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_world():
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from PDFLocal"}


def test_dashboard_renders():
    response = client.get("/")
    assert response.status_code == 200
    assert "PDFLocal" in response.text
