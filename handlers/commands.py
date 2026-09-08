from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from config import bot
from datetime import datetime

import random

commands_router = Router()



jokes = [
    "Программист — это устройство, которое превращает кофе в код.",
    "Как называется программист, который не пьёт кофе? Спящий.",
    "Всю ночь чинил баг, который сам же и создал.",
    "Есть только 10 типов людей: те, кто понимает двоичный код, и те, кто нет.",
    "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 == DEC 25.",
]



@commands_router.message(Command('start'))
async def start_handlers(message: Message):
    await message.answer(text='Привет')


@commands_router.message(Command('help'))
async def help_handler(message: Message):
    text = (
        'Первый бот группы 69-2\n\n'
        '/start — приветствие\n'
        '/help — список команд\n'
        '/mem — картинка\n'
        '/sticker — стикер\n'
        '/time — текущая дата и время\n'
        '/random — случайное число от 1 до 100\n'
        '/joke — случайная шутка\n'
        '/form — заполнение анкеты'
    )
    await bot.send_message(chat_id=message.chat.id, text=text)


@commands_router.message(F.text == 'Привет')
async def hello_text_handler(message: Message):
    await message.answer('hello')


@commands_router.message(Command('mem'))
async def mem_handler(message: Message):
    photo_mem = FSInputFile('media/mem.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo_mem)


@commands_router.message(Command('sticker'))
async def sticker_handler(message: Message):
    await message.answer_sticker(sticker='CAACAgIAAxkBAAMpapp7YE6kD95hwfcfi7d6aoNTtXAAAlEUAAKUxWFJztlv4bpoU9c9BA')


@commands_router.message(F.sticker)
async def get_sticker_id_handler(message: Message):
    await message.answer(f'ID этого стикера - {message.sticker.file_id}')


@commands_router.message(Command('time'))
async def time_handler(message: Message):
    now = datetime.now()
    await message.answer(f'Сейчас: {now.strftime("%d.%m.%Y %H:%M")}')


@commands_router.message(Command('random'))
async def random_handler(message: Message):
    number = random.randint(1, 100)
    await message.answer(f'Твоё случайное число: {number}')


@commands_router.message(Command('joke'))
async def joke_handler(message: Message):
    joke = random.choice(jokes)
    await message.answer(joke)


