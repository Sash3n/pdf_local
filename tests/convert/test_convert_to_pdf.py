import shutil

import pikepdf
import pytest

from app.core.convert_to_pdf import jpg_to_pdf, office_to_pdf
from app.core.libreoffice import LibreOfficeNotFound, find_soffice


def test_jpg_to_pdf(make_image, tmp_path):
    images = [make_image(f"img_{i}.jpg") for i in range(2)]
    output = tmp_path / "converted.pdf"

    jpg_to_pdf(images, output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 2


@pytest.mark.skipif(find_soffice() is not None, reason="LibreOffice is installed")
def test_office_to_pdf_raises_when_libreoffice_missing(tmp_path):
    fake_docx = tmp_path / "doc.docx"
    fake_docx.write_bytes(b"not a real docx")

    with pytest.raises(LibreOfficeNotFound):
        office_to_pdf(fake_docx, tmp_path / "out")


@pytest.mark.skipif(find_soffice() is None, reason="LibreOffice is not installed")
def test_office_to_pdf_converts_docx(tmp_path):
    from docx import Document

    doc = Document()
    doc.add_paragraph("Hello PDFLocal")
    docx_path = tmp_path / "doc.docx"
    doc.save(docx_path)

    output = office_to_pdf(docx_path, tmp_path / "out")

    assert output.exists()
    shutil.rmtree(tmp_path / "out", ignore_errors=True)
