import sqlite3
from pathlib import Path




DB_PATH = Path(__file__).parent / "trial_lessons.db"



def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trial_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                phone TEXT NOT NULL
            )
            """
        )
        conn.commit()