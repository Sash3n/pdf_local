from pathlib import Path

from app.core.libreoffice import convert_via_libreoffice
from app.core.organize import images_to_pdf


def jpg_to_pdf(image_paths: list[Path], output: Path) -> Path:
    return images_to_pdf(image_paths, output)


def office_to_pdf(input_path: Path, output_dir: Path) -> Path:
    return convert_via_libreoffice(input_path, output_dir, target_format="pdf")


def html_to_pdf(input_path: Path, output_dir: Path) -> Path:
    return convert_via_libreoffice(input_path, output_dir, target_format="pdf")
