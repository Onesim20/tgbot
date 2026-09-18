from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.shop_db import add_product_db, get_products_with_details

router = Router()


class AddProduct(StatesGroup):
    name = State()
    price = State()
    description = State()
    product_id = State()   
    category = State()
    photo = State()


@router.message(Command("cancel"), StateFilter(AddProduct))
async def cancel_add_product(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Добавление товара отменено.")


@router.message(Command("add_product2"))
async def start_add_product(message: Message, state: FSMContext) -> None:
    await state.set_state(AddProduct.name)
    await message.answer("Введите название товара (или /cancel для отмены):")


@router.message(StateFilter(AddProduct.name))
async def add_name(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Название должно быть текстом. Введите название товара:")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(AddProduct.price)
    await message.answer("Введите цену товара (только число):")


@router.message(StateFilter(AddProduct.price))
async def add_price(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.isdigit():
        await message.answer("Цена должна быть числом. Попробуйте ещё раз:")
        return
    await state.update_data(price=int(message.text))
    await state.set_state(AddProduct.description)
    await message.answer("Напишите описание товара:")


@router.message(StateFilter(AddProduct.description))
async def add_description(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Описание должно быть текстом. Попробуйте ещё раз:")
        return
    await state.update_data(description=message.text.strip())
    await state.set_state(AddProduct.product_id)
    await message.answer("Введите артикул товара (число, должно быть уникальным):")


@router.message(StateFilter(AddProduct.product_id))
async def add_product_id(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.isdigit():
        await message.answer("Артикул должен быть числом. Попробуйте ещё раз:")
        return
    await state.update_data(product_id=int(message.text))
    await state.set_state(AddProduct.category)
    await message.answer("Введите категорию товара:")


@router.message(StateFilter(AddProduct.category))
async def add_category(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Категория должна быть текстом. Попробуйте ещё раз:")
        return
    await state.update_data(category=message.text.strip())
    await state.set_state(AddProduct.photo)
    await message.answer("Отправьте фото товара:")


@router.message(StateFilter(AddProduct.photo))
async def add_photo(message: Message, state: FSMContext) -> None:
    if not message.photo:
        await message.answer("Нужно отправить именно фото. Попробуйте ещё раз:")
        return

    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()

    await add_product_db(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        product_id=data["product_id"],
        category=data["category"],
        photo=data["photo"],
    )

    await message.answer_photo(
        photo=data["photo"],
        caption=(
            "Товар добавлен в базу ✅"
            f"\nНазвание — {data['name']}"
            f"\nЦена — {data['price']}"
            f"\nОписание — {data['description']}"
            f"\nАртикул — {data['product_id']}"
            f"\nКатегория — {data['category']}"
        ),
    )
    await state.clear()


@router.message(Command("catalog"))
async def cmd_catalog(message: Message) -> None:
    rows = await get_products_with_details()
    if not rows:
        await message.answer("В каталоге пока нет товаров. Добавьте через /add_product2")
        return

    lines = ["<b>Каталог товаров (INNER JOIN двух таблиц):</b>", ""]
    for name, price, description, category, product_id in rows:
        lines.append(
            f"• <b>{name}</b> — {price} руб.\n"
            f"  Категория: {category}\n"
            f"  Описание: {description}\n"
            f"  Артикул: {product_id}"
        )
    await message.answer("\n".join(lines))
