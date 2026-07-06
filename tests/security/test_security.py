import pikepdf

from app.core.security import (
    protect_pdf,
    sign_pdf_with_certificate,
    sign_pdf_with_image,
    sign_pdf_with_text,
    unlock_pdf,
)


def test_protect_and_unlock_pdf(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=1)
    protected = tmp_path / "protected.pdf"
    unlocked = tmp_path / "unlocked.pdf"

    protect_pdf(source, protected, user_password="secret123")

    with pikepdf.open(protected, password="secret123") as pdf:
        assert len(pdf.pages) == 1

    unlock_pdf(protected, unlocked, password="secret123")

    with pikepdf.open(unlocked) as pdf:
        assert len(pdf.pages) == 1


def test_sign_pdf_with_image(make_pdf, make_image, tmp_path):
    source = make_pdf("source.pdf", pages=1)
    signature = make_image("signature.png")
    output = tmp_path / "signed.pdf"

    sign_pdf_with_image(source, output, page_number=1, image_path=signature, box=(10, 10, 100, 60))

    assert output.exists()


def test_sign_pdf_with_text(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=1)
    output = tmp_path / "signed.pdf"

    sign_pdf_with_text(source, output, page_number=1, text="John Doe", x=10, y=10)

    import fitz

    with fitz.open(output) as doc:
        assert "John Doe" in doc[0].get_text()


def test_sign_pdf_with_certificate(make_pdf, make_pfx, tmp_path):
    source = make_pdf("source.pdf", pages=1)
    pfx_path = make_pfx("test-password")
    output = tmp_path / "signed.pdf"

    sign_pdf_with_certificate(source, output, pfx_path=pfx_path, pfx_password="test-password")

    assert output.exists()
    assert output.stat().st_size > source.stat().st_size
