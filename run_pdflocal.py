"""Entry point for the packaged PyInstaller build. Not used in normal dev mode
(use `python -m uvicorn app.main:app --reload` for that instead)."""

import webbrowser
from threading import Timer

import uvicorn

from app.main import app

HOST = "127.0.0.1"
PORT = 8000


def _open_browser() -> None:
    webbrowser.open(f"http://{HOST}:{PORT}")


def main() -> None:
    Timer(1.5, _open_browser).start()
    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
