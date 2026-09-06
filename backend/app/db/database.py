import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "backend" / "policy.db"


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with dictionary-like row access."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the policies table if it does not already exist."""
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            region TEXT NOT NULL,
            daily_limit_usd REAL NOT NULL,
            currency TEXT NOT NULL,
            notes TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()