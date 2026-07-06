import io
from pathlib import Path

import fitz
import pikepdf


def compress_pdf(path: Path, output: Path, image_quality: int = 60) -> Path:
    with pikepdf.open(path) as pdf:
        for page in pdf.pages:
            for raw_image in page.get_images().values():
                pdf_image = pikepdf.PdfImage(raw_image)
                try:
                    pil_image = pdf_image.as_pil_image().convert("RGB")
                except Exception:
                    continue
                buffer = io.BytesIO()
                pil_image.save(buffer, format="JPEG", quality=image_quality)
                raw_image.write(buffer.getvalue(), filter=pikepdf.Name("/DCTDecode"))
                raw_image.ColorSpace = pikepdf.Name("/DeviceRGB")
        pdf.save(
            output, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate
        )
    return output


def repair_pdf(path: Path, output: Path) -> Path:
    try:
        with pikepdf.open(path) as pdf:
            pdf.save(output)
        return output
    except pikepdf.PdfError:
        doc = fitz.open(path)
        doc.save(output)
        doc.close()
        return output
