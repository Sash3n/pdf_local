import fitz
import pikepdf

from app.core.optimize import compress_pdf, repair_pdf


def _make_pdf_with_image(tmp_path, make_image):
    image_path = make_image("photo.jpg", size=(800, 800))
    doc = fitz.open()
    page = doc.new_page()
    page.insert_image(fitz.Rect(0, 0, 400, 400), filename=str(image_path))
    path = tmp_path / "with_image.pdf"
    doc.save(path)
    doc.close()
    return path


def test_compress_pdf_reduces_size(tmp_path, make_image):
    source = _make_pdf_with_image(tmp_path, make_image)
    output = tmp_path / "compressed.pdf"

    compress_pdf(source, output, image_quality=30)

    assert output.exists()
    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 1


def test_repair_pdf_returns_valid_pdf(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=2)
    output = tmp_path / "repaired.pdf"

    repair_pdf(source, output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 2
