# PDFLocal — Project Specification

**Repo:** `pdf_local` — `https://github.com/Sash3n/pdf_local.git`
**Owner:** Sashen
**Status:** Draft v1.0 — ready for Phase 0 scaffolding

## 1. Purpose

A fully local, offline-first PDF toolkit that replicates and extends the feature set of ilovepdf.com,
without ever sending a document to a third-party server. All processing (merge, split, convert, OCR,
compress, sign, etc.) happens on the user's own machine. The only "cloud" dependency permitted anywhere
in this project is the local machine itself.

Non-goals for v1: no user accounts/multi-tenancy, no server deployment, no telemetry leaving the device,
no AI/cloud LLM calls of any kind.

## 2. Confirmed Decisions

| Area | Decision |
|---|---|
| Architecture | Local web app — Python backend, browser-rendered UI at `localhost` |
| Target OS | Cross-platform (Windows / macOS / Linux) from v1 |
| Packaging | Standalone installer via PyInstaller, built from v1 |
| Office conversions | Depend on a local LibreOffice install (headless `soffice`) for best fidelity |
| Sign PDF | Draw/type/image signatures **and** digital certificate (PKI/X.509) signing |
| Scan to PDF | Images-to-PDF only (overlaps with JPG→PDF; no physical scanner/TWAIN integration in v1) |
| OCR | Tesseract, English only for v1 |
| Analytics | Files processed per tool, storage saved, processing time trends, error/failure rates, most-used tools ranking — all in a local SQLite DB |
| Sensitive file handling | Temp files deleted immediately after each operation completes (or fails) |
| Batch processing | Supported from v1, for every tool |
| Testing | pytest, TDD (tests written before implementation per feature), 90%+ coverage enforced in CI |
| CI | GitHub Actions — must pass before merge; review is optional (solo dev) |
| Security scanning | `pip-audit` + `bandit` in CI, build fails on high-severity findings |
| Versioning | Semantic versioning (`MAJOR.MINOR.PATCH`) with a `CHANGELOG.md` per release |
| License | MIT |
| Dark/light mode | Sourced directly from the Stitch design system (already includes both) |

## 3. Tech Stack

**Backend**
- Python 3.11+
- FastAPI (async, auto OpenAPI docs, plays well with background tasks for batch jobs)
- Uvicorn as the local server
- SQLite (via `sqlalchemy` or plain `sqlite3`) for analytics/history metadata only — never file contents
- Jinja2 templates for server-rendered pages, progressively enhanced with vanilla JS (no heavy SPA
  framework needed for a local tool; keeps the PyInstaller bundle small)

**Frontend**
- Tailwind CSS — **compiled via Tailwind CLI**, not the CDN `<script>` tag used in the raw Stitch
  export (the CDN build is dev-only and Tailwind explicitly warns against shipping it; the packaged
  app should ship a compiled, purged CSS file). The exact design tokens from `DESIGN.md` are ported
  into `tailwind.config.js` unchanged.
- Material Symbols Outlined (self-hosted font subset, not the Google Fonts CDN link used in the
  export — no external network calls at runtime in the packaged app)
- Inter (self-hosted, same reasoning)
- Class-based dark mode (`darkMode: "class"`), matching the export's `<html class="light">` /
  `dark` toggle pattern already implemented in the theme switch on the Privacy & Settings screen

**PDF/document engines (all local, no cloud APIs)**

| Feature | Library / tool |
|---|---|
| Merge / Split / Remove / Extract / Organize / Rotate / Crop / Page numbers / Watermark | `pikepdf` (qpdf bindings) + `PyMuPDF` (`fitz`) for rendering/thumbnails |
| Compress | `PyMuPDF` recompression + image downsampling via `Pillow` |
| Repair | `pikepdf` (`qpdf --recover`) with `PyMuPDF` fallback re-save |
| OCR | `pytesseract` + Tesseract OCR engine (English data pack) |
| JPG ⇄ PDF | `Pillow` + `PyMuPDF` |
| Word ⇄ PDF, PowerPoint ⇄ PDF, Excel ⇄ PDF, HTML → PDF | LibreOffice headless (`soffice --headless --convert-to`) |
| PDF → Word | `pdf2docx` |
| PDF → Excel | `pdfplumber` / `camelot-py` for table extraction → `openpyxl` |
| PDF → Markdown | `PyMuPDF` text/structure extraction → custom Markdown formatter (headings, tables, lists preserved) |
| Protect / Unlock (password) | `pikepdf` (AES-256 encryption) |
| Sign (drawn/typed/image) | `PyMuPDF` overlay + `Pillow` |
| Sign (digital certificate / PKI) | `pyHanko` (X.509 signing, PAdES-compliant) |
| Thumbnails/previews | `PyMuPDF` page rasterization |

**Packaging & tooling**
- PyInstaller (one-folder or one-file build per OS)
- `pytest`, `pytest-cov`, `pytest-asyncio`
- `bandit`, `pip-audit`
- `ruff` (lint) + `black` (format) — recommended alongside the security tools
- GitHub Actions (`.github/workflows/ci.yml`)

## 4. Directory Structure

```
pdf_local/
├── app/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── api/                     # route modules, one per tool category
│   │   ├── organize.py
│   │   ├── optimize.py
│   │   ├── convert.py
│   │   ├── edit.py
│   │   ├── security.py
│   │   └── intelligence.py      # PDF → Markdown
│   ├── core/                    # shared engine wrappers (pikepdf, PyMuPDF, LibreOffice bridge)
│   ├── analytics/                # SQLite models + metrics collection
│   ├── templates/                # Jinja2 pages, ported from Stitch HTML exports
│   └── static/
│       ├── css/                  # compiled Tailwind output
│       ├── fonts/                # self-hosted Inter + Material Symbols
│       └── js/
├── docs/
│   ├── spec.md                   # this file
│   ├── design.md                 # gitignored — internal design reference
│   ├── research.md                # library/tool sources used
│   └── stitch/                   # gitignored — raw Stitch exports
├── tests/
│   ├── organize/
│   ├── optimize/
│   ├── convert/
│   ├── edit/
│   ├── security/
│   ├── intelligence/
│   └── fixtures/                 # sample PDFs/docs for testing
├── .github/workflows/ci.yml
├── .gitignore
├── CHANGELOG.md
├── LICENSE                       # MIT
├── README.md
├── pyproject.toml
└── requirements.txt
```

## 5. Feature Roadmap (phased, with check-ins between phases)

Each phase = one feature branch (or a small cluster of closely related tools), built TDD-first,
merged to `dev` once CI is green, with its own README section and CHANGELOG entry.

- **Phase 0 — Scaffolding:** repo init, git flow, CI pipeline, base FastAPI app, Tailwind build
  pipeline, dark/light theme toggle, shell layout (sidebar + top bar) ported from the Dashboard screen.
- **Phase 1 — Organize PDF:** Merge, Split, Remove pages, Extract pages, Organize (reorder), Scan-to-PDF
  (images→PDF). Reference: the "Merge PDF" screen/HTML export is the canonical workspace pattern
  (drop zone → selected-files grid → sticky action bar) reused for every tool in this phase.
- **Phase 2 — Optimize PDF:** Compress, Repair.
- **Phase 3 — Convert to PDF:** JPG, Word, PowerPoint, Excel, HTML → PDF (LibreOffice bridge built here).
- **Phase 4 — Convert from PDF:** PDF → JPG, Word, Excel.
- **Phase 5 — Edit PDF:** Rotate, Add page numbers, Add watermark, Crop, basic text/annotation edit.
- **Phase 6 — PDF Security:** Unlock, Protect (password/AES-256), Sign (drawn/typed/image +
  PKI/X.509 via pyHanko).
- **Phase 7 — PDF Intelligence:** PDF → Markdown.
- **Phase 8 — Analytics Dashboard:** SQLite metrics store + dashboard charts (files processed per tool,
  storage saved, processing time trends, error rates, most-used tools), matching the visual language
  of the Intelligence Hub / Dashboard screens (stat cards, "Local Processing" badges, tonal cards).
- **Phase 9 — Packaging:** PyInstaller builds for Windows/macOS/Linux, installer polish, first
  tagged `v1.0.0` release.

Stretch / explicitly deferred (seen in the Stitch "Intelligence Hub" mockup but not in your original
tool list — flagging for a future decision, not blocking v1): AI Summarizer, Translate PDF, Neural
Semantic Search, AI Smart Redaction, PDF Forms, PDF/A conversion, Compare PDF. These would require an
on-device LLM (e.g. a local llama.cpp/GGUF model) and are a materially bigger scope increase — worth
a dedicated spec of their own later.

## 6. Design System Reference

Full tokens live in `docs/design.md` (gitignored) sourced from your Stitch `DESIGN.md` — summary here
for context:

- **Style:** "Privacy-First Minimalism" — Apple-esque, high negative space, disciplined color use,
  red/orange reserved strictly for destructive actions.
- **Typography:** Inter only, steep hierarchy (48px display down to 12px label-caps).
- **Color:** deep indigo (`#131f5d`) primary, vivid indigo (`#2e00c8`) secondary, near-black navy for
  dark-mode surfaces (never pure black), `success-teal` (`#05CD99`) for safe/complete states, error
  red (`#ba1a1a`) reserved for destructive actions.
- **Shape:** 12px standard radius, 16px for buttons, 8px for inputs.
- **Elevation:** tonal layers + soft ambient shadows (15% opacity / 20px blur) for cards; glassmorphism
  (20px backdrop blur) for nav bars and the sticky action bar.
- **Grid:** 1280px max container, 12-column grid, cards span 3/4/6/12 cols across desktop/tablet/mobile.
- **Recurring components confirmed from the exports/screens:**
  - Fixed left sidebar (Dashboard / Tools / Intelligence / Privacy nav, "Upgrade to Pro" — **remove
    all Pro/upsell/paywall copy and buttons**, since this is a fully local, non-commercial tool; keep
    the visual slot but repurpose or drop it).
  - Top bar: search, privacy shield icon, dark-mode toggle (moon icon), avatar.
  - "Local Processing Active" badge under the logo, and an "ENCRYPTED & LOCAL" / "Local Processing"
    pill on every tool workspace — keep this pattern, it's a good honest trust signal and happens
    to be true for this build.
  - Tool workspace pattern (seen in Merge PDF): header + description + drop zone ("Drop PDFs here /
    or click to browse") → selected-files thumbnail grid with page/size metadata → sticky bottom
    action bar with file count, combined size, and the primary action button.
  - Dashboard: category cards (Organize, Optimize, Convert, Edit Content) each listing their tools
    as sub-rows/buttons — maps directly to Phase 1–5 tool groupings.
  - Settings/Privacy screen: engine priority selector, on-device OCR status + language count, data
    retention mode, account/local-install management. Adapt "Account Management" section to reflect
    that this is a single local user with no cloud account — replace with local profile/preferences
    only (no subscription, no "Terminate Account" cloud language).

## 7. Analytics & Dashboard Details

SQLite table `tool_runs`: `id, tool_name, started_at, finished_at, input_file_count, input_size_bytes,
output_size_bytes, status (success/failure), error_message (nullable)`. No document content or
filenames beyond what's needed for the run are persisted; retention follows the "delete immediately"
policy for the actual files — only these run metrics persist locally for the dashboard.

Dashboard shows: files processed per tool (bar chart), storage saved via compression (before/after,
cumulative), processing time trends (line chart over time), error/failure rate (%, per tool), and a
most-used-tools ranking (leaderboard/top list).

## 8. Security Considerations

- No outbound network calls at runtime (fonts/Tailwind self-hosted, no CDN dependency in production build).
- Temp files written to an OS temp dir, deleted immediately after each operation (success or failure).
- Password/PKI operations never log the password/private key material.
- Uploaded file size/page-count sanity limits enforced server-side to avoid resource exhaustion.
- `bandit` static analysis + `pip-audit` dependency scanning in CI, failing the build on high-severity
  findings.
- Filenames sanitized before any filesystem write.

## 9. Testing Strategy

- TDD: for each tool, write failing tests first against `tests/<category>/test_<tool>.py`, using
  fixture PDFs/docs in `tests/fixtures/`.
- Unit tests per engine wrapper (e.g. merge logic in isolation) + integration tests per API route.
- Coverage gate: 90%+ enforced in CI (`pytest --cov=app --cov-fail-under=90`).
- Batch-processing paths tested explicitly (multi-file input for every tool).

## 10. Git Workflow

```
main        ── protected, release-only, tagged (vX.Y.Z)
  └─ dev     ── integration branch, CI must pass before merge from any feature branch
       └─ feature/<name>   ── one per phase/tool cluster, never deleted after merge
```

- No `Co-Authored-By` trailers, no em/en dashes in commit messages — plain, direct commit text.
- CI (GitHub Actions) must pass on every PR into `dev` and every merge from `dev` into `main`;
  review is optional per your call, but CI is a hard gate.
- Each feature branch gets its own README section update (see §11) and a `CHANGELOG.md` entry before
  merging.

Initial setup commands:
```bash
git init
git branch -M main
git checkout -b dev
git remote add origin https://github.com/Sash3n/pdf_local.git
```

## 11. README Requirements (updated per feature, professionally, no co-authorship lines)

Each merge to `dev` should leave `README.md` current with:
- Project overview and current feature status (table of implemented tools)
- Architecture summary (diagram or description) reflecting §4
- Setup/run instructions (dev mode + how to build the installer)
- Testing instructions and current coverage
- Security/privacy notes (local-only processing, no telemetry)
- Roadmap / future plans (linking to §5)
- Research/reference links (linking to `docs/research.md`)
- License (MIT)

## 12. `.gitignore` (key entries)

```
docs/design.md
docs/stitch/
__pycache__/
*.pyc
.venv/
venv/
dist/
build/
*.spec
instance/*.db
.env
node_modules/
```

## 13. Open Questions Before Phase 0 Starts

1. Confirm you're fine dropping all "Upgrade to Pro" / subscription / "Professional Plan" UI copy
   from the ported screens (§6) — this is a fully local, license-free tool with no paid tier.
2. LibreOffice must be installed on the host machine for Phase 3/4 conversions to work — should the
   installer (Phase 9) attempt to detect/prompt for it, or is a documented manual prerequisite fine
   for v1?
3. For PKI signing (Phase 6), do you already have a certificate workflow in mind (self-signed for
   personal use, or a specific CA), or should the tool just support importing a `.pfx`/`.p12` and
   leave certificate acquisition entirely up to the user?
