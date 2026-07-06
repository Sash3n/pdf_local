from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import (
    convert_from_pdf,
    convert_to_pdf,
    edit,
    intelligence,
    optimize,
    organize,
    security,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="PDFLocal")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(organize.router)
app.include_router(optimize.router)
app.include_router(convert_to_pdf.router)
app.include_router(convert_from_pdf.router)
app.include_router(edit.router)
app.include_router(security.router)
app.include_router(intelligence.router)


@app.get("/api/hello")
def hello_world() -> dict[str, str]:
    return {"message": "Hello from PDFLocal"}


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "dashboard.html", {})


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
