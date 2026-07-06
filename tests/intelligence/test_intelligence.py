import fitz

from app.core.intelligence import pdf_to_markdown, pdf_to_markdown_file


def _make_structured_pdf(tmp_path):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Document Title", fontsize=24)
    page.insert_text((72, 110), "This is body text.", fontsize=11)
    page.insert_text((72, 130), "- First bullet", fontsize=11)
    path = tmp_path / "structured.pdf"
    doc.save(path)
    doc.close()
    return path


def test_pdf_to_markdown_detects_heading(tmp_path):
    source = _make_structured_pdf(tmp_path)

    markdown = pdf_to_markdown(source)

    assert "# Document Title" in markdown
    assert "This is body text." in markdown


def test_pdf_to_markdown_detects_bullet(tmp_path):
    source = _make_structured_pdf(tmp_path)

    markdown = pdf_to_markdown(source)

    assert "- First bullet" in markdown


def test_pdf_to_markdown_file(tmp_path):
    source = _make_structured_pdf(tmp_path)
    output = tmp_path / "output.md"

    pdf_to_markdown_file(source, output)

    assert output.exists()
    assert "# Document Title" in output.read_text(encoding="utf-8")
