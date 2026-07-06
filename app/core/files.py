import re
import shutil
import tempfile
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

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
