# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Phase 1: Organize PDF tools - Merge, Split, Remove pages, Extract pages, Organize (reorder),
  Scan to PDF (images to PDF), backed by pikepdf and Pillow, with API routes under
  `/api/organize/*` and full unit/integration test coverage.
- Phase 0: project scaffolding - git workflow, directory structure, FastAPI hello-world app,
  Tailwind CLI build pipeline, base page shell with dark/light theme toggle, pytest with
  coverage reporting, GitHub Actions CI (lint, tests, security scans).
