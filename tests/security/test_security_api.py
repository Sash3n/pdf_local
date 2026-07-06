from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_protect_and_unlock_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    protect_response = client.post(
        "/api/security/protect",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"user_password": "secret123"},
    )
    assert protect_response.status_code == 200

    unlock_response = client.post(
        "/api/security/unlock",
        files={"file": ("protected.pdf", protect_response.content, "application/pdf")},
        data={"password": "secret123"},
    )
    assert unlock_response.status_code == 200


def test_sign_image_endpoint(make_pdf, make_image):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    signature = make_image("signature.png").read_bytes()
    response = client.post(
        "/api/security/sign/image",
        files={
            "file": ("source.pdf", data, "application/pdf"),
            "signature": ("signature.png", signature, "image/png"),
        },
        data={"page": "1", "x0": "10", "y0": "10", "x1": "100", "y1": "60"},
    )
    assert response.status_code == 200


def test_sign_text_endpoint(make_pdf):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    response = client.post(
        "/api/security/sign/text",
        files={"file": ("source.pdf", data, "application/pdf")},
        data={"text": "Jane Doe", "page": "1", "x": "10", "y": "10"},
    )
    assert response.status_code == 200


def test_sign_certificate_endpoint(make_pdf, make_pfx):
    data = make_pdf("source.pdf", pages=1).read_bytes()
    pfx_data = make_pfx("test-password").read_bytes()
    response = client.post(
        "/api/security/sign/certificate",
        files={
            "file": ("source.pdf", data, "application/pdf"),
            "pfx": ("signer.pfx", pfx_data, "application/x-pkcs12"),
        },
        data={"pfx_password": "test-password"},
    )
    assert response.status_code == 200
