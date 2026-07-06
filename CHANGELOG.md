# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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
