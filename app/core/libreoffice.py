import shutil
import subprocess
from pathlib import Path


class LibreOfficeNotFound(RuntimeError):
    pass


def find_soffice() -> str | None:
    return shutil.which("soffice") or shutil.which("libreoffice")


def convert_via_libreoffice(input_path: Path, output_dir: Path, target_format: str = "pdf") -> Path:
    soffice = find_soffice()
    if not soffice:
        raise LibreOfficeNotFound(
            "LibreOffice (soffice) is not installed. It is a required manual prerequisite "
            "for Word/PowerPoint/Excel/HTML conversions - see docs/spec.md section 13."
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            soffice,
            "--headless",
            "--convert-to",
            target_format,
            "--outdir",
            str(output_dir),
            str(input_path),
        ],
        check=True,
        timeout=120,
        capture_output=True,
    )
    output_path = output_dir / f"{input_path.stem}.{target_format}"
    if not output_path.exists():
        raise RuntimeError("LibreOffice conversion did not produce the expected output file")
    return output_path
