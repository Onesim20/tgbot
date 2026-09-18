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


insert_product= 'INSERT INTO products (name,price, product_id, photo) VALUES (?, ?, ?, ?)'
insert_products_detail = 'INSERT INTO  (name, age, phone) VALUES (?, ?, ?)'


# ===================== Урок 5: JOIN (products + products_detail) =====================

CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    product_id INTEGER NOT NULL
)
"""

CREATE_PRODUCTS_DETAIL_TABLE = """
CREATE TABLE IF NOT EXISTS products_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    product_id INTEGER NOT NULL,
    category TEXT
)
"""

INSERT_PRODUCT = "INSERT INTO products (name, price, product_id) VALUES (?, ?, ?)"

INSERT_PRODUCT_DETAIL = "INSERT INTO products_detail (description, product_id, category) VALUES (?, ?, ?)"

SELECT_PRODUCTS_JOIN = """
SELECT products.name, products.price, products_detail.category, products_detail.description
FROM products
INNER JOIN products_detail ON products.product_id = products_detail.product_id
ORDER BY products.id
"""