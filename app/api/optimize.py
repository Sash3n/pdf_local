from fastapi import APIRouter, Form, UploadFile

from app.core.files import file_response, save_uploads, temp_workspace
from app.core.optimize import compress_pdf, repair_pdf

router = APIRouter(prefix="/api/optimize", tags=["optimize"])


@router.post("/compress")
async def compress(file: UploadFile, quality: int = Form(60)):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "compressed.pdf"
        compress_pdf(path, output, image_quality=quality)
        return file_response(output, "compressed.pdf")


@router.post("/repair")
async def repair(file: UploadFile):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / "repaired.pdf"
        repair_pdf(path, output)
        return file_response(output, "repaired.pdf")
