from pathlib import Path

import fitz
import pikepdf


def unlock_pdf(path: Path, output: Path, password: str) -> Path:
    with pikepdf.open(path, password=password) as pdf:
        pdf.save(output)
    return output


def protect_pdf(
    path: Path, output: Path, user_password: str, owner_password: str | None = None
) -> Path:
    owner_password = owner_password or user_password
    with pikepdf.open(path) as pdf:
        pdf.save(
            output,
            encryption=pikepdf.Encryption(user=user_password, owner=owner_password, R=6),
        )
    return output


def sign_pdf_with_image(
    path: Path,
    output: Path,
    page_number: int,
    image_path: Path,
    box: tuple[float, float, float, float],
) -> Path:
    with fitz.open(path) as doc:
        page = doc[page_number - 1]
        page.insert_image(fitz.Rect(*box), filename=str(image_path))
        doc.save(output)
    return output


def sign_pdf_with_text(
    path: Path,
    output: Path,
    page_number: int,
    text: str,
    x: float,
    y: float,
    fontsize: int = 24,
) -> Path:
    with fitz.open(path) as doc:
        page = doc[page_number - 1]
        page.insert_text((x, y), text, fontsize=fontsize, fontname="Times-Italic")
        doc.save(output)
    return output


def sign_pdf_with_certificate(
    path: Path, output: Path, pfx_path: Path, pfx_password: str, field_name: str = "Signature1"
) -> Path:
    from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
    from pyhanko.sign import signers

    signer = signers.SimpleSigner.load_pkcs12(
        pfx_file=str(pfx_path), passphrase=pfx_password.encode()
    )
    with open(path, "rb") as infile:
        writer = IncrementalPdfFileWriter(infile)
        with open(output, "wb") as outfile:
            signers.sign_pdf(
                writer,
                signers.PdfSignatureMetadata(field_name=field_name),
                signer=signer,
                output=outfile,
            )
    return output
