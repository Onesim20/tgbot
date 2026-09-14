from database import queries
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class TrialLesson(StatesGroup):
    name = State()
    age = State()
    phone = State()


router_fsm = Router()



@router_fsm.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Сейчас нечего отменять.')
        return

    await state.clear()
    await message.answer('Анкета отменена. Чтобы начать заново — /form')


@router_fsm.message(Command('form'))
async def form_start(message: Message, state: FSMContext):
    await message.answer('Записываемся на пробное занятие!\nКак вас зовут?')
    await state.set_state(TrialLesson.name)


@router_fsm.message(TrialLesson.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько вам лет?')
    await state.set_state(TrialLesson.age)


@router_fsm.message(TrialLesson.age)
async def form_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Возраст должен быть числом. Попробуйте ещё раз:')
        return

    age = int(message.text)
    if age <= 0 or age > 120:
        await message.answer('Введите реальный возраст:')
        return

    await state.update_data(age=age)
    await message.answer('Укажите номер телефона для связи:')
    await state.set_state(TrialLesson.phone)


@router_fsm.message(TrialLesson.phone)
async def form_phone(message: Message, state: FSMContext):
    data = await state.update_data(phone=message.text)

    queries.add_trial_lesson(name=data["name"], age=data["age"], phone=data["phone"])

    await message.answer(
        'Запись оформлена!\n\n'
        f'Имя: {data["name"]}\n'
        f'Возраст: {data["age"]}\n'
        f'Телефон: {data["phone"]}'
    )
    await state.clear()

@router_fsm.message(Command('records'))
async def records_handler(message: Message):
    records = queries.get_all_trial_lessons()
    if not records:
        await message.answer('Записей пока нет.')
        return

    lines = [f"{i}. {name}, {age} лет, тел. {phone}" for i, name, age, phone in records]
    await message.answer('\n'.join(lines))