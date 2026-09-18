from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import main_db


class AddProduct(StatesGroup):
    name = State()
    price = State()
    description = State()
    product_id = State()   # артикул — общее поле для JOIN
    category = State()


router_addproduct = Router()


@router_addproduct.message(Command('add_product'))
async def add_start_fsm(message: Message, state: FSMContext):
    await message.answer('Введите название товара:')
    await state.set_state(AddProduct.name)


@router_addproduct.message(AddProduct.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите цену товара:')
    await state.set_state(AddProduct.price)


@router_addproduct.message(AddProduct.price)
async def add_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Цена должна быть числом. Попробуйте ещё раз:')
        return
    await state.update_data(price=int(message.text))
    await message.answer("Напишите описание товара:")
    await state.set_state(AddProduct.description)


@router_addproduct.message(AddProduct.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите артикул товара (число, общее поле для двух таблиц):')
    await state.set_state(AddProduct.product_id)


@router_addproduct.message(AddProduct.product_id)
async def add_product_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Артикул должен быть числом. Попробуйте ещё раз:')
        return
    await state.update_data(product_id=int(message.text))
    await message.answer('Введите категорию товара:')
    await state.set_state(AddProduct.category)


@router_addproduct.message(AddProduct.category)
async def add_category(message: Message, state: FSMContext):
    data = await state.update_data(category=message.text)

    await main_db.add_product(
        name=data['name'], price=data['price'], product_id=data['product_id'],
    )
    await main_db.add_product_detail(
        description=data['description'], product_id=data['product_id'], category=data['category'],
    )

    await message.answer(
        'Товар добавлен!\n\n'
        f"Название: {data['name']}\n"
        f"Цена: {data['price']}\n"
        f"Описание: {data['description']}\n"
        f"Артикул: {data['product_id']}\n"
        f"Категория: {data['category']}"
    )
    await state.clear()


@router_addproduct.message(Command('products'))
async def products_list_handler(message: Message):
    rows = await main_db.get_all_products()
    if not rows:
        await message.answer('Товаров пока нет.')
        return
    lines = [f"{name} — {price}\nКатегория: {category}\n{description}" for name, price, category, description in rows]
    await message.answer('\n\n'.join(lines))