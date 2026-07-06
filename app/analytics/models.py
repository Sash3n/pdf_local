from pathlib import Path

from sqlalchemy import BigInteger, Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DB_PATH = Path("instance") / "analytics.db"


class ToolRun(Base):
    __tablename__ = "tool_runs"

    id = Column(Integer, primary_key=True)
    tool_name = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    input_file_count = Column(Integer, nullable=False, default=0)
    input_size_bytes = Column(BigInteger, nullable=False, default=0)
    output_size_bytes = Column(BigInteger, nullable=True)
    status = Column(String, nullable=False)
    error_message = Column(String, nullable=True)


def get_engine(db_path: Path = DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{db_path}")


_engine = None
_SessionLocal = None


def init_db(db_path: Path = DB_PATH):
    global _engine, _SessionLocal
    _engine = get_engine(db_path)
    Base.metadata.create_all(_engine)
    _SessionLocal = sessionmaker(bind=_engine)
    return _SessionLocal


def get_session():
    global _SessionLocal
    if _SessionLocal is None:
        init_db()
    return _SessionLocal()


def reset_analytics_state():
    """Test-only helper to force re-initialization against a fresh DB path."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None
