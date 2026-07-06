import pikepdf

from app.core.organize import (
    extract_pages,
    images_to_pdf,
    merge_pdfs,
    remove_pages,
    reorder_pages,
    split_pdf,
)


def test_merge_pdfs(make_pdf, tmp_path):
    a = make_pdf("a.pdf", pages=2)
    b = make_pdf("b.pdf", pages=3)
    output = tmp_path / "merged.pdf"

    merge_pdfs([a, b], output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 5


def test_merge_pdfs_batch_of_many_files(make_pdf, tmp_path):
    paths = [make_pdf(f"file_{i}.pdf", pages=1) for i in range(5)]
    output = tmp_path / "merged.pdf"

    merge_pdfs(paths, output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 5


def test_split_pdf(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=4)
    output_dir = tmp_path / "split"

    outputs = split_pdf(source, output_dir)

    assert len(outputs) == 4
    for out_path in outputs:
        with pikepdf.open(out_path) as pdf:
            assert len(pdf.pages) == 1


def test_remove_pages(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=5)
    output = tmp_path / "removed.pdf"

    remove_pages(source, [2, 4], output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 3


def test_extract_pages(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=5)
    output = tmp_path / "extracted.pdf"

    extract_pages(source, [1, 3], output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 2


def test_reorder_pages(make_pdf, tmp_path):
    source = make_pdf("source.pdf", pages=3)
    output = tmp_path / "reordered.pdf"

    reorder_pages(source, [3, 1, 2], output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 3


def test_images_to_pdf(make_image, tmp_path):
    images = [make_image(f"img_{i}.jpg") for i in range(3)]
    output = tmp_path / "images.pdf"

    images_to_pdf(images, output)

    with pikepdf.open(output) as pdf:
        assert len(pdf.pages) == 3
