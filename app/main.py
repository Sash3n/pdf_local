import json
import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.analytics.middleware import AnalyticsMiddleware
from app.analytics.queries import (
    error_rate_per_tool,
    most_used_tools,
    storage_saved_bytes,
)
from app.api import (
    analytics,
    convert_from_pdf,
    convert_to_pdf,
    edit,
    intelligence,
    optimize,
    organize,
    security,
)
from app.core.tool_catalog import CATEGORIES, get_tool

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="PDFLocal")

app.add_middleware(AnalyticsMiddleware)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(organize.router)
app.include_router(optimize.router)
app.include_router(convert_to_pdf.router)
app.include_router(convert_from_pdf.router)
app.include_router(edit.router)
app.include_router(security.router)
app.include_router(intelligence.router)
app.include_router(analytics.router)


@app.get("/api/hello")
def hello_world() -> dict[str, str]:
    return {"message": "Hello from PDFLocal"}


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "dashboard.html", {})


@app.get("/tools", response_class=HTMLResponse)
def tools_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "tools.html", {"categories": CATEGORIES})


@app.get("/tools/{slug}", response_class=HTMLResponse)
def tool_page(request: Request, slug: str) -> HTMLResponse:
    tool = get_tool(slug)
    if tool is None:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {slug}")
    config = json.dumps({"endpoint": tool.endpoint, "multiple": tool.multiple})
    return templates.TemplateResponse(
        request, "tool_workspace.html", {"tool": tool, "tool_config_json": config}
    )


@app.get("/security/sign", response_class=HTMLResponse)
def sign_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "sign.html", {})


@app.get("/privacy", response_class=HTMLResponse)
def privacy_page(request: Request) -> HTMLResponse:
    engines = [
        {
            "label": "pikepdf (qpdf)",
            "description": "Merge, split, organize, compress, encrypt/decrypt",
            "available": True,
        },
        {
            "label": "PyMuPDF",
            "description": "Rendering, rotate, watermark, crop, page numbers, rasterization",
            "available": True,
        },
        {
            "label": "LibreOffice",
            "description": "Word, PowerPoint, Excel, and HTML to PDF conversion",
            "available": shutil.which("soffice") is not None
            or shutil.which("libreoffice") is not None,
        },
        {
            "label": "Tesseract OCR",
            "description": "On-device text recognition (English)",
            "available": shutil.which("tesseract") is not None,
        },
    ]
    return templates.TemplateResponse(request, "privacy.html", {"engines": engines})


@app.get("/analytics", response_class=HTMLResponse)
def analytics_dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "analytics.html",
        {
            "most_used_tools": most_used_tools(),
            "storage_saved": storage_saved_bytes(),
            "error_rate_per_tool": error_rate_per_tool(),
        },
    )


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
