from fastapi import APIRouter, UploadFile
from fastapi.responses import Response

from app.core.files import save_uploads, temp_workspace
from app.core.intelligence import pdf_to_markdown

router = APIRouter(prefix="/api/intelligence", tags=["intelligence"])


@router.post("/pdf-to-markdown")
async def pdf_to_markdown_route(file: UploadFile):
    with temp_workspace() as workspace:
        [path] = await save_uploads([file], workspace)
        markdown = pdf_to_markdown(path)
        return Response(content=markdown, media_type="text/markdown")
