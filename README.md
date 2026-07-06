# PDFLocal

A fully local, offline-first PDF toolkit that replicates and extends the feature set of
ilovepdf.com, without ever sending a document to a third-party server. All processing (merge,
split, convert, OCR, compress, sign, etc.) happens on your own machine. The only "cloud"
dependency permitted anywhere in this project is the local machine itself.

## Feature Status

| Phase | Area | Status |
|---|---|---|
| 0 | Scaffolding (app shell, CI, build pipeline) | Done |
| 1 | Organize PDF (Merge, Split, Remove, Extract, Organize, Scan to PDF) | Done |
| 2 | Optimize PDF (Compress, Repair) | Done |
| 3 | Convert to PDF (JPG, Word, PowerPoint, Excel, HTML) | Done (Word/PPT/Excel/HTML need LibreOffice installed) |
| 4 | Convert from PDF (JPG, Word, Excel) | Done |
| 5 | Edit PDF (Rotate, Page numbers, Watermark, Crop, Edit) | Done |
| 6 | PDF Security (Unlock, Protect, Sign) | Done |
| 7 | PDF Intelligence (PDF to Markdown) | Not started |
| 8 | Analytics Dashboard | Not started |
| 9 | Packaging (PyInstaller) | Not started |

See `docs/spec.md` section 5 for the full roadmap.

## Architecture

- **Backend:** FastAPI (Python 3.11+) served by Uvicorn, with Jinja2-rendered pages progressively
  enhanced with vanilla JS. SQLite stores analytics/history metadata only, never document content.
- **Frontend:** Tailwind CSS compiled via the Tailwind CLI (not the CDN script tag), with
  class-based dark mode. Inter and Material Symbols Outlined are self-hosted, so the app makes
  zero outbound network calls at runtime.
- **PDF/document engines:** pikepdf, PyMuPDF, Pillow, Tesseract/pytesseract, LibreOffice headless,
  pdf2docx, pdfplumber/camelot, openpyxl, pyHanko - all running locally. See `docs/spec.md`
  section 3 for the full mapping of features to libraries.

```
pdf_local/
├── app/            # FastAPI app, routes, core engine wrappers, analytics, templates, static assets
├── docs/           # spec, research links (design.md and stitch/ are gitignored)
├── tests/          # pytest suite, mirrors app/api categories
├── .github/        # CI workflow
├── pyproject.toml  # pytest/ruff/black/bandit config
└── requirements.txt
```

## Setup

Requires Python 3.11+ and Node.js (for the Tailwind CLI build).

```bash
python -m venv .venv
source .venv/Scripts/activate   # .venv/bin/activate on macOS/Linux
pip install -r requirements.txt

npm install
npm run build:css               # compiles Tailwind output.css and self-hosts fonts
```

Run the dev server:

```bash
python -m uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000`.

## Testing

```bash
pytest
```

Runs the full suite with coverage reporting (`pytest-cov`, configured in `pyproject.toml`).
The project enforces a 90%+ coverage gate in CI once enough tools are implemented to make that
threshold meaningful (see `docs/spec.md` section 9); Phase 0 has no gate yet, but coverage is
already being measured and reported.

Lint and format checks:

```bash
ruff check .
black --check .
```

Security scans:

```bash
bandit -r app -ll
pip-audit -r requirements.txt
```

## Security & Privacy

- No outbound network calls at runtime; fonts and CSS are self-hosted and compiled, not pulled
  from a CDN.
- Uploaded files are processed in a temp directory and deleted immediately after each operation,
  success or failure.
- No user accounts, no telemetry, no AI/cloud LLM calls anywhere in this project.
- `bandit` and `pip-audit` run in CI on every PR; the build fails on high-severity findings.

## Roadmap

Full phased roadmap lives in `docs/spec.md` section 5, covering Organize/Optimize/Convert/Edit/
Security/Intelligence tools through to a PyInstaller-packaged v1.0.0 release.

## Research & References

Library and tool sources are tracked in `docs/research.md`.

## License

MIT - see `LICENSE`.
