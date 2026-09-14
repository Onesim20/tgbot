from typing import List, Tuple

from database.db import get_connection


def add_trial_lesson(name: str, age: int, phone: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO trial_lessons (name, age, phone) VALUES (?, ?, ?)",
            (name, age, phone),
        )
        conn.commit()


def get_all_trial_lessons() -> List[Tuple[int, str, int, str]]:
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, name, age, phone FROM trial_lessons ORDER BY id"
        )
        return cursor.fetchall()