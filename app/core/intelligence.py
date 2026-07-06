import statistics
from pathlib import Path

import fitz


def pdf_to_markdown(path: Path) -> str:
    lines_out: list[str] = []
    with fitz.open(path) as doc:
        for page in doc:
            page_dict = page.get_text("dict")
            sizes = [
                span["size"]
                for block in page_dict["blocks"]
                if "lines" in block
                for line in block["lines"]
                for span in line["spans"]
            ]
            median_size = statistics.median(sizes) if sizes else 12

            for block in page_dict["blocks"]:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    text = "".join(span["text"] for span in line["spans"]).strip()
                    if not text:
                        continue
                    max_size = max((span["size"] for span in line["spans"]), default=median_size)
                    if max_size >= median_size * 1.5:
                        lines_out.append(f"# {text}")
                    elif max_size >= median_size * 1.2:
                        lines_out.append(f"## {text}")
                    elif text.startswith(("- ", "* ", "• ")):
                        lines_out.append(f"- {text[2:].strip()}")
                    else:
                        lines_out.append(text)
                lines_out.append("")
    return "\n".join(lines_out).strip() + "\n"


def pdf_to_markdown_file(path: Path, output: Path) -> Path:
    output.write_text(pdf_to_markdown(path), encoding="utf-8")
    return output
