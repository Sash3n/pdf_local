from pathlib import Path

import fitz


def rotate_pages(path: Path, output: Path, angle: int, pages: list[int] | None = None) -> Path:
    with fitz.open(path) as doc:
        target_pages = pages or list(range(1, doc.page_count + 1))
        for page_num in target_pages:
            page = doc[page_num - 1]
            page.set_rotation((page.rotation + angle) % 360)
        doc.save(output)
    return output


def add_page_numbers(path: Path, output: Path, start: int = 1) -> Path:
    with fitz.open(path) as doc:
        for index, page in enumerate(doc):
            rect = page.rect
            text = str(start + index)
            page.insert_text((rect.width / 2, rect.height - 36), text, fontsize=10)
        doc.save(output)
    return output


def add_watermark(path: Path, output: Path, text: str, opacity: float = 0.3) -> Path:
    with fitz.open(path) as doc:
        for page in doc:
            rect = page.rect
            page.insert_text(
                (rect.width / 4, rect.height / 2),
                text,
                fontsize=40,
                rotate=0,
                color=(0.6, 0.6, 0.6),
                fill_opacity=opacity,
            )
        doc.save(output)
    return output


def crop_pages(
    path: Path,
    output: Path,
    box: tuple[float, float, float, float],
    pages: list[int] | None = None,
) -> Path:
    with fitz.open(path) as doc:
        target_pages = pages or list(range(1, doc.page_count + 1))
        for page_num in target_pages:
            page = doc[page_num - 1]
            page.set_cropbox(fitz.Rect(*box))
        doc.save(output)
    return output


def edit_text(path: Path, output: Path, page_number: int, text: str, x: float, y: float) -> Path:
    with fitz.open(path) as doc:
        page = doc[page_number - 1]
        page.insert_text((x, y), text, fontsize=12)
        doc.save(output)
    return output
