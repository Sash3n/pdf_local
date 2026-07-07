# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Frontend: wired real pages for every tool built in Phases 1-9, replacing the placeholder
  `href="#"` nav links left over from Phase 0. A config-driven `tool_workspace.html` template
  (`app/core/tool_catalog.py`) renders each tool at its own URL matching the canonical Merge PDF
  workspace fidelity (drop zone, file cards with drag-reorder, sticky action bar), with a
  generic upload/download JS controller (`app/static/js/tool-workspace.js`,
  `response-handler.js`) that auto-downloads binary results or previews text results (e.g.
  Markdown) inline. Sign PDF gets a bespoke page (`sign.html`) with Draw/Upload Image/Type/
  Certificate modes, including a canvas signature pad. Added `/tools` (index), `/security/sign`,
  and `/privacy` (Settings/Privacy, with live LibreOffice/Tesseract detection) pages, and
  rebuilt the Dashboard's category cards to link into real tools instead of a stale "ships in
  the next phase" placeholder. Also fixed `/api/organize/split`, which previously returned only
  a page count with no downloadable file - it now returns a zip of the split pages.

- Phase 9: Packaging - PyInstaller spec (`pdflocal.spec`) bundling templates, compiled CSS,
  and self-hosted fonts into a standalone executable that launches a local server and opens
  the browser automatically. Verified end-to-end on Windows (build runs, serves all routes
  and static assets). `.github/workflows/release.yml` builds Windows/macOS/Linux artifacts
  in a CI matrix whenever a `v*.*.*` tag is pushed; macOS/Linux builds have not been run or
  verified locally since this environment is Windows-only.
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

### Fixed
- Dark mode on the new frontend pages initially used light-mode-only design tokens
  (`surface-container`/`surface-container-high`) as `dark:` variants, since DESIGN.md never
  defines a distinct dark palette; this produced unreadable near-white-on-light-gray text.
  Fixed by using the genuine dark tokens (`inverse-surface`/`inverse-on-surface`) established
  in the Phase 0 shell, verified visually via a headless-browser screenshot pass.
