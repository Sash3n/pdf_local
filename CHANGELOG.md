# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Phase 8: Analytics Dashboard - SQLite `tool_runs` metrics store (SQLAlchemy), populated
  automatically by an HTTP middleware that wraps every `/api/*` POST route (no per-route
  instrumentation needed), plus a `/api/analytics/summary` endpoint and a server-rendered
  `/analytics` dashboard page (most-used tools, storage saved via compression, error rate
  per tool). No document content or filenames are ever persisted, only run metadata.
- Phase 7: PDF Intelligence - PDF to Markdown using PyMuPDF structured text extraction with
  relative font-size heading detection and bullet list preservation, under
  `/api/intelligence/pdf-to-markdown`.
- Phase 6: PDF Security tools - Unlock and Protect (pikepdf AES-256), drawn/typed/image
  signatures (PyMuPDF overlay), and digital certificate (PAdES/X.509) signing via pyHanko,
  under `/api/security/*`. Certificate signing runs in a thread pool since pyHanko's signer
  is not natively async-compatible.
- Phase 5: Edit PDF tools - Rotate, Add page numbers, Add watermark, Crop, and basic text
  insertion, all via PyMuPDF, under `/api/edit/*`.
- Phase 4: Convert from PDF tools - PDF to JPG (PyMuPDF rasterization, zipped output), PDF to
  Word (pdf2docx), PDF to Excel (pdfplumber table extraction into openpyxl workbooks), under
  `/api/convert-from-pdf/*`.
- Phase 3: Convert to PDF tools - JPG to PDF (reuses the Organize image pipeline), and a
  LibreOffice headless bridge (`app/core/libreoffice.py`) powering Word, PowerPoint, Excel,
  and HTML to PDF. LibreOffice is a documented manual prerequisite (see spec.md section 13);
  routes return 503 with a clear message when `soffice` is not found on the host.
- Phase 2: Optimize PDF tools - Compress (image downsampling via pikepdf/Pillow, stream
  recompression) and Repair (pikepdf recovery with PyMuPDF fallback re-save), under
  `/api/optimize/*`.
- Phase 1: Organize PDF tools - Merge, Split, Remove pages, Extract pages, Organize (reorder),
  Scan to PDF (images to PDF), backed by pikepdf and Pillow, with API routes under
  `/api/organize/*` and full unit/integration test coverage.
- Phase 0: project scaffolding - git workflow, directory structure, FastAPI hello-world app,
  Tailwind CLI build pipeline, base page shell with dark/light theme toggle, pytest with
  coverage reporting, GitHub Actions CI (lint, tests, security scans).
