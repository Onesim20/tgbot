from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AddProduct(StatesGroup):
    name = State()
    price = State()
    description = State()


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
    await state.update_data(price=message.text)
    await message.answer("Напишите описание товара:")
    await state.set_state(AddProduct.description)


@router_addproduct.message(AddProduct.description)
async def add_description(message: Message, state: FSMContext):
    data = await state.update_data(description=message.text)

    await message.answer(f"Данные товара: Название - {data['name']} Цена - {data['price']} Описание - {data['description']}")
    await message.answer(f"Данные товара: \nНазвание - {data['name']} \nЦена - {data['price']} \nОписание - {data['description']}")

    await state.clear()
    await state.clear()
