from collections.abc import Callable
from pathlib import Path

import fitz
import pytest


@pytest.fixture
def make_pdf(tmp_path: Path) -> Callable[..., Path]:
    def _make_pdf(name: str = "sample.pdf", pages: int = 3, text: str | None = None) -> Path:
        doc = fitz.open()
        for i in range(pages):
            page = doc.new_page()
            page.insert_text((72, 72), text or f"Page {i + 1}")
        path = tmp_path / name
        doc.save(path)
        doc.close()
        return path

    return _make_pdf


@pytest.fixture
def make_image(tmp_path: Path) -> Callable[..., Path]:
    from PIL import Image

    def _make_image(
        name: str = "sample.jpg", size: tuple[int, int] = (200, 200), color=(255, 0, 0)
    ) -> Path:
        path = tmp_path / name
        Image.new("RGB", size, color).save(path)
        return path

    return _make_image
