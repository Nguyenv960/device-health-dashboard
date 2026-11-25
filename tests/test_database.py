import sqlite3
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PROJECT_ROOT / "migrations" / "001_initial.sql"

@pytest.fixture
def connection():
    database = sqlite3.connect(":memory:")
    database.execute("PRAGMA foreign_keys = ON;")
    database.executescript(SCHEMA_PATH.read_text(encoding="utf-8-sig"))

    try:
        yield database
    finally:
        database.close()

def test_collection_run_requires_exisiting_device(connection):
    with pytest.raises(sqlite3.IntegrityError, match = "FOREIGN KEY"):
        