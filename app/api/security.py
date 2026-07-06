from fastapi import APIRouter, Form, UploadFile
from starlette.concurrency import run_in_threadpool

from app.core.files import file_response, save_uploads, temp_workspace
from app.core.security import (
    protect_pdf,
    sign_pdf_with_certificate,
    sign_pdf_with_image,
    sign_pdf_with_text,
    unlock_pdf,
)

router = APIRouter(prefix="/api/security", tags=["security"])


@router.post("/unlock")
async def unlock(file: UploadFile, password: str = Form(...)):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "unlocked.pdf"
        unlock_pdf(path, output, password=password)
        return file_response(output, "unlocked.pdf")


@router.post("/protect")
async def protect(
    file: UploadFile, user_password: str = Form(...), owner_password: str | None = Form(None)
):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "protected.pdf"
        protect_pdf(path, output, user_password=user_password, owner_password=owner_password)
        return file_response(output, "protected.pdf")


@router.post("/sign/image")
async def sign_image(
    file: UploadFile,
    signature: UploadFile,
    page: int = Form(...),
    x0: float = Form(...),
    y0: float = Form(...),
    x1: float = Form(...),
    y1: float = Form(...),
):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        [sig_path] = await save_uploads([signature], workspace)
        output = workspace / "signed.pdf"
        sign_pdf_with_image(
            path, output, page_number=page, image_path=sig_path, box=(x0, y0, x1, y1)
        )
        return file_response(output, "signed.pdf")


@router.post("/sign/text")
async def sign_text(
    file: UploadFile,
    text: str = Form(...),
    page: int = Form(...),
    x: float = Form(...),
    y: float = Form(...),
):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "signed.pdf"
        sign_pdf_with_text(path, output, page_number=page, text=text, x=x, y=y)
        return file_response(output, "signed.pdf")


@router.post("/sign/certificate")
async def sign_certificate(file: UploadFile, pfx: UploadFile, pfx_password: str = Form(...)):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        [pfx_path] = await save_uploads([pfx], workspace)
        output = workspace / "signed.pdf"
        await run_in_threadpool(sign_pdf_with_certificate, path, output, pfx_path, pfx_password)
        return file_response(output, "signed.pdf")
