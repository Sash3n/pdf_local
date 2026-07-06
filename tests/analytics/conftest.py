from pathlib import Path

import pytest

from app.analytics import models


@pytest.fixture(autouse=True)
def isolated_analytics_db(tmp_path: Path, monkeypatch):
    db_path = tmp_path / "analytics-test.db"
    models.reset_analytics_state()
    models.init_db(db_path)
    yield db_path
    models.reset_analytics_state()
