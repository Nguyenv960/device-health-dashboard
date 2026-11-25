import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "device_health.db"
SCHEMA_PATH = PROJECT_ROOT / "migrations" / "001_initial.sql"

def initialize_database():
    schema = SCHEMA_PATH.read_text(encoding="utf-8-sig")
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON;")

        connection.executescript("BEGIN;\n" + schema + "\nCOMMIT;")

        foreign_keys_enabled = connection.execute("PRAGMA foreign_keys;").fetchone()[0]

        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()

        print(f"Database: {DATABASE_PATH}")
        print(f"Foreign keys enabled: {foreign_keys_enabled}")
        print("Tables: ")

        for (table_name,) in tables:
            print(f"- {table_name}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

if __name__ == "__main__":
    initialize_database()