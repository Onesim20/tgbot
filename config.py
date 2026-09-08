from aiogram import Bot, Dispatcher
from decouple import config

Admin = []

token_bot = config("TOKEN")

bot = Bot(token=token_bot)
dp = Dispatcher()