from pathlib import Path

import pikepdf
from PIL import Image


def merge_pdfs(paths: list[Path], output: Path) -> Path:
    pdf = pikepdf.Pdf.new()
    for path in paths:
        with pikepdf.open(path) as src:
            pdf.pages.extend(src.pages)
    pdf.save(output)
    pdf.close()
    return output


def split_pdf(path: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    with pikepdf.open(path) as src:
        for index, page in enumerate(src.pages):
            single = pikepdf.Pdf.new()
            single.pages.append(page)
            out_path = output_dir / f"page_{index + 1}.pdf"
            single.save(out_path)
            single.close()
            outputs.append(out_path)
    return outputs


def remove_pages(path: Path, pages: list[int], output: Path) -> Path:
    with pikepdf.open(path) as src:
        remove_set = {p - 1 for p in pages}
        for index in sorted(remove_set, reverse=True):
            del src.pages[index]
        src.save(output)
    return output


def extract_pages(path: Path, pages: list[int], output: Path) -> Path:
    with pikepdf.open(path) as src:
        extracted = pikepdf.Pdf.new()
        for page_num in pages:
            extracted.pages.append(src.pages[page_num - 1])
        extracted.save(output)
        extracted.close()
    return output


def reorder_pages(path: Path, order: list[int], output: Path) -> Path:
    with pikepdf.open(path) as src:
        reordered = pikepdf.Pdf.new()
        for page_num in order:
            reordered.pages.append(src.pages[page_num - 1])
        reordered.save(output)
        reordered.close()
    return output


def images_to_pdf(image_paths: list[Path], output: Path) -> Path:
    images = [Image.open(p).convert("RGB") for p in image_paths]
    first, rest = images[0], images[1:]
    first.save(output, save_all=True, append_images=rest)
    return output
