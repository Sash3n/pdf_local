from fastapi import APIRouter, Form, UploadFile

from app.core.files import file_response, save_uploads, temp_workspace
from app.core.organize import (
    extract_pages,
    images_to_pdf,
    merge_pdfs,
    remove_pages,
    reorder_pages,
    split_pdf,
)

router = APIRouter(prefix="/api/organize", tags=["organize"])


@router.post("/merge")
async def merge(files: list[UploadFile]):
    with temp_workspace() as workspace:
        paths = await save_uploads(files, workspace)
        output = workspace / "merged.pdf"
        merge_pdfs(paths, output)
        return file_response(output, "merged.pdf")


@router.post("/split")
async def split(file: UploadFile):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        outputs = split_pdf(path, workspace / "split")
        return {"pages": len(outputs)}


@router.post("/remove")
async def remove(file: UploadFile, pages: str = Form(...)):
    page_numbers = [int(p) for p in pages.split(",") if p]
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "removed.pdf"
        remove_pages(path, page_numbers, output)
        return file_response(output, "removed.pdf")


@router.post("/extract")
async def extract(file: UploadFile, pages: str = Form(...)):
    page_numbers = [int(p) for p in pages.split(",") if p]
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "extracted.pdf"
        extract_pages(path, page_numbers, output)
        return file_response(output, "extracted.pdf")


@router.post("/reorder")
async def reorder(file: UploadFile, order: str = Form(...)):
    page_numbers = [int(p) for p in order.split(",") if p]
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "reordered.pdf"
        reorder_pages(path, page_numbers, output)
        return file_response(output, "reordered.pdf")


@router.post("/scan-to-pdf")
async def scan_to_pdf(files: list[UploadFile]):
    with temp_workspace() as workspace:
        paths = await save_uploads(files, workspace)
        output = workspace / "scanned.pdf"
        images_to_pdf(paths, output)
        return file_response(output, "scanned.pdf")
