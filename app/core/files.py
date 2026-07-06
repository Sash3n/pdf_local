import re
import shutil
import tempfile
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from fastapi.responses import Response

if TYPE_CHECKING:
    from fastapi import UploadFile

_UNSAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")


def sanitize_filename(name: str) -> str:
    name = Path(name).name
    name = _UNSAFE_CHARS.sub("_", name)
    return name or "file"


@contextmanager
def temp_workspace() -> Iterator[Path]:
    workspace = Path(tempfile.gettempdir()) / f"pdflocal-{uuid.uuid4().hex}"
    workspace.mkdir(parents=True, exist_ok=True)
    try:
        yield workspace
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


async def save_uploads(files: "list[UploadFile]", workspace: Path) -> list[Path]:
    saved = []
    for upload in files:
        name = sanitize_filename(upload.filename or "file")
        path = workspace / name
        path.write_bytes(await upload.read())
        saved.append(path)
    return saved


def file_response(path: Path, filename: str, media_type: str = "application/pdf") -> Response:
    data = path.read_bytes()
    return Response(
        content=data,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
