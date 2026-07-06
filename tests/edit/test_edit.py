import fitz

from app.core.edit import add_page_numbers, add_watermark, crop_pages, edit_text, rotate_pages


def test_rotate_pages(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=2)
    output = tmp_path / "rotated.pdf"

    rotate_pages(source, output, angle=90)

    with fitz.open(output) as doc:
        assert doc[0].rotation == 90
        assert doc[1].rotation == 90


def test_rotate_specific_pages(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=3)
    output = tmp_path / "rotated.pdf"

    rotate_pages(source, output, angle=180, pages=[2])

    with fitz.open(output) as doc:
        assert doc[0].rotation == 0
        assert doc[1].rotation == 180
        assert doc[2].rotation == 0


def test_add_page_numbers(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=3)
    output = tmp_path / "numbered.pdf"

    add_page_numbers(source, output)

    with fitz.open(output) as doc:
        assert "1" in doc[0].get_text()
        assert "3" in doc[2].get_text()


def test_add_watermark(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=1)
    output = tmp_path / "watermarked.pdf"

    add_watermark(source, output, text="CONFIDENTIAL")

    with fitz.open(output) as doc:
        assert "CONFIDENTIAL" in doc[0].get_text()


def test_crop_pages(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=1)
    output = tmp_path / "cropped.pdf"

    crop_pages(source, output, box=(0, 0, 200, 200))

    with fitz.open(output) as doc:
        assert doc[0].cropbox.width == 200
        assert doc[0].cropbox.height == 200


def test_edit_text(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=1)
    output = tmp_path / "edited.pdf"

    edit_text(source, output, page_number=1, text="Inserted text", x=50, y=50)

    with fitz.open(output) as doc:
        assert "Inserted text" in doc[0].get_text()
