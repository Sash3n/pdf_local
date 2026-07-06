from fastapi import APIRouter, HTTPException, UploadFile

from app.core.convert_to_pdf import html_to_pdf, jpg_to_pdf, office_to_pdf
from app.core.files import file_response, save_uploads, temp_workspace
from app.core.libreoffice import LibreOfficeNotFound

router = APIRouter(prefix="/api/convert-to-pdf", tags=["convert-to-pdf"])


@router.post("/jpg")
async def jpg(files: list[UploadFile]):
    with temp_workspace() as workspace:
        paths = await save_uploads(files, workspace)
        output = workspace / "converted.pdf"
        jpg_to_pdf(paths, output)
        return file_response(output, "converted.pdf")


def _office_route(convert_fn):
    async def handler(file: UploadFile):
        with temp_workspace() as workspace:
            [path] = await save_uploads([file], workspace)
            try:
                output = convert_fn(path, workspace / "out")
            except LibreOfficeNotFound as exc:
                raise HTTPException(status_code=503, detail=str(exc)) from exc
            return file_response(output, f"{path.stem}.pdf")

    return handler


router.add_api_route("/word", _office_route(office_to_pdf), methods=["POST"])
router.add_api_route("/powerpoint", _office_route(office_to_pdf), methods=["POST"])
router.add_api_route("/excel", _office_route(office_to_pdf), methods=["POST"])
router.add_api_route("/html", _office_route(html_to_pdf), methods=["POST"])
