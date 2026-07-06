from fastapi import APIRouter, Form, UploadFile

from app.core.edit import add_page_numbers, add_watermark, crop_pages, edit_text, rotate_pages
from app.core.files import file_response, save_uploads, temp_workspace

router = APIRouter(prefix="/api/edit", tags=["edit"])


@router.post("/rotate")
async def rotate(file: UploadFile, angle: int = Form(...), pages: str | None = Form(None)):
    page_numbers = [int(p) for p in pages.split(",") if p] if pages else None
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "rotated.pdf"
        rotate_pages(path, output, angle=angle, pages=page_numbers)
        return file_response(output, "rotated.pdf")


@router.post("/page-numbers")
async def page_numbers(file: UploadFile, start: int = Form(1)):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "numbered.pdf"
        add_page_numbers(path, output, start=start)
        return file_response(output, "numbered.pdf")


@router.post("/watermark")
async def watermark(file: UploadFile, text: str = Form(...), opacity: float = Form(0.3)):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "watermarked.pdf"
        add_watermark(path, output, text=text, opacity=opacity)
        return file_response(output, "watermarked.pdf")


@router.post("/crop")
async def crop(
    file: UploadFile,
    x0: float = Form(...),
    y0: float = Form(...),
    x1: float = Form(...),
    y1: float = Form(...),
):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "cropped.pdf"
        crop_pages(path, output, box=(x0, y0, x1, y1))
        return file_response(output, "cropped.pdf")


@router.post("/text")
async def text(
    file: UploadFile,
    page: int = Form(...),
    content: str = Form(...),
    x: float = Form(...),
    y: float = Form(...),
):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "edited.pdf"
        edit_text(path, output, page_number=page, text=content, x=x, y=y)
        return file_response(output, "edited.pdf")
