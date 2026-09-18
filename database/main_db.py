import aiosqlite
from pathlib import Path

from database.queries import (
    CREATE_PRODUCTS_TABLE,
    CREATE_PRODUCTS_DETAIL_TABLE,
    INSERT_PRODUCT,
    INSERT_PRODUCT_DETAIL,
    SELECT_PRODUCTS_JOIN,
)

PRODUCTS_DB_PATH = Path(__file__).parent / "products.db"


async def init_products_db() -> None:
    async with aiosqlite.connect(PRODUCTS_DB_PATH) as conn:
        await conn.execute(CREATE_PRODUCTS_TABLE)
        await conn.execute(CREATE_PRODUCTS_DETAIL_TABLE)
        await conn.commit()


async def add_product(name: str, price: int, product_id: int) -> None:
    async with aiosqlite.connect(PRODUCTS_DB_PATH) as conn:
        await conn.execute(INSERT_PRODUCT, (name, price, product_id))
        await conn.commit()


async def add_product_detail(description: str, product_id: int, category: str) -> None:
    async with aiosqlite.connect(PRODUCTS_DB_PATH) as conn:
        await conn.execute(INSERT_PRODUCT_DETAIL, (description, product_id, category))
        await conn.commit()


async def get_all_products():
    async with aiosqlite.connect(PRODUCTS_DB_PATH) as conn:
        cursor = await conn.execute(SELECT_PRODUCTS_JOIN)
        return await cursor.fetchall()