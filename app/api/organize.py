from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import Response

from app.core.files import sanitize_filename, temp_workspace
from app.core.organize import (
    extract_pages,
    images_to_pdf,
    merge_pdfs,
    remove_pages,
    reorder_pages,
    split_pdf,
)

router = APIRouter(prefix="/api/organize", tags=["organize"])


async def _save_uploads(files: list[UploadFile], workspace) -> list:
    saved = []
    for upload in files:
        name = sanitize_filename(upload.filename or "file.pdf")
        path = workspace / name
        path.write_bytes(await upload.read())
        saved.append(path)
    return saved


def _pdf_response(path, filename: str) -> Response:
    data = path.read_bytes()
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/merge")
async def merge(files: list[UploadFile]):
    with temp_workspace() as workspace:
        paths = await _save_uploads(files, workspace)
        output = workspace / "merged.pdf"
        merge_pdfs(paths, output)
        return _pdf_response(output, "merged.pdf")


@router.post("/split")
async def split(file: UploadFile):
    with temp_workspace() as workspace:
        [path] = await _save_uploads([file], workspace)
        outputs = split_pdf(path, workspace / "split")
        return {"pages": len(outputs)}


@router.post("/remove")
async def remove(file: UploadFile, pages: str = Form(...)):
    page_numbers = [int(p) for p in pages.split(",") if p]
    with temp_workspace() as workspace:
        [path] = await _save_uploads([file], workspace)
        output = workspace / "removed.pdf"
        remove_pages(path, page_numbers, output)
        return _pdf_response(output, "removed.pdf")


@router.post("/extract")
async def extract(file: UploadFile, pages: str = Form(...)):
    page_numbers = [int(p) for p in pages.split(",") if p]
    with temp_workspace() as workspace:
        [path] = await _save_uploads([file], workspace)
        output = workspace / "extracted.pdf"
        extract_pages(path, page_numbers, output)
        return _pdf_response(output, "extracted.pdf")


@router.post("/reorder")
async def reorder(file: UploadFile, order: str = Form(...)):
    page_numbers = [int(p) for p in order.split(",") if p]
    with temp_workspace() as workspace:
        [path] = await _save_uploads([file], workspace)
        output = workspace / "reordered.pdf"
        reorder_pages(path, page_numbers, output)
        return _pdf_response(output, "reordered.pdf")


@router.post("/scan-to-pdf")
async def scan_to_pdf(files: list[UploadFile]):
    with temp_workspace() as workspace:
        paths = await _save_uploads(files, workspace)
        output = workspace / "scanned.pdf"
        images_to_pdf(paths, output)
        return _pdf_response(output, "scanned.pdf")
