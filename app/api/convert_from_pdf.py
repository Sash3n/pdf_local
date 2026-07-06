import zipfile

from fastapi import APIRouter, UploadFile

from app.core.convert_from_pdf import pdf_to_excel, pdf_to_jpg, pdf_to_word
from app.core.files import file_response, save_uploads, temp_workspace

router = APIRouter(prefix="/api/convert-from-pdf", tags=["convert-from-pdf"])


@router.post("/jpg")
async def jpg(file: UploadFile):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        images = pdf_to_jpg(path, workspace / "pages")
        archive = workspace / "pages.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            for image in images:
                zf.write(image, arcname=image.name)
        return file_response(archive, "pages.zip", media_type="application/zip")


@router.post("/word")
async def word(file: UploadFile):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / f"{path.stem}.docx"
        pdf_to_word(path, output)
        return file_response(
            output,
            output.name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )


@router.post("/excel")
async def excel(file: UploadFile):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        output = workspace / f"{path.stem}.xlsx"
        pdf_to_excel(path, output)
        return file_response(
            output,
            output.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
