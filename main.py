from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from decouple import config
from datetime import datetime
import random
import asyncio
import logging

token_bot = config("TOKEN")
bot = Bot(token=token_bot)
dp = Dispatcher()

router_main = Router()
dp.include_router(router_main)

jokes = [
    "Программист — это устройство, которое превращает кофе в код.",
    "Как называется программист, который не пьёт кофе? Спящий.",
    "Всю ночь чинил баг, который сам же и создал.",
    "Есть только 10 типов людей: те, кто понимает двоичный код, и те, кто нет.",
    "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 == DEC 25.",
]


@router_main.message(Command('start'))
async def start_handlers(message: Message):
    await message.answer(text='Привет')


@router_main.message(Command('help'))
async def help_handler(message: Message):
    text = (
        'Первый бот группы 69-2\n\n'
        '/start — приветствие\n'
        '/help — список команд\n'
        '/mem — картинка\n'
        '/sticker — стикер\n'
        '/time — текущая дата и время\n'
        '/random — случайное число от 1 до 100\n'
        '/joke — случайная шутка'
    )
    await bot.send_message(chat_id=message.chat.id, text=text)


@router_main.message(F.text == 'Привет')
async def hello_text_handler(message: Message):
    await message.answer('hello')


@router_main.message(Command('mem'))
async def mem_handler(message: Message):
    photo_mem = FSInputFile('media/mem.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo_mem)


@router_main.message(Command('sticker'))
async def sticker_handler(message: Message):
    await message.answer_sticker(sticker='CAACAgIAAxkBAAMpapp7YE6kD95hwfcfi7d6aoNTtXAAAlEUAAKUxWFJztlv4bpoU9c9BA')


@router_main.message(F.sticker)
async def get_sticker_id_handler(message: Message):
    await message.answer(f'ID этого стикера - {message.sticker.file_id}')


@router_main.message(Command('time'))
async def time_handler(message: Message):
    now = datetime.now()
    await message.answer(f'Сейчас: {now.strftime("%d.%m.%Y %H:%M")}')


@router_main.message(Command('random'))
async def random_handler(message: Message):
    number = random.randint(1, 100)
    await message.answer(f'Твоё случайное число: {number}')


@router_main.message(Command('joke'))
async def joke_handler(message: Message):
    joke = random.choice(jokes)
    await message.answer(joke)


@router_main.message(F.text)
async def echo_handler(message: Message):
    await message.answer(f'Такой команды нет - {message.text}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
