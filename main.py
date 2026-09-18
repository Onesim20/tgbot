import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from config import bot, dp, Admin
from database.db import create_table
from database import main_db          
from handlers import commands, echo, fsm_add_products, fsm

async def set_commands() -> None:
    bot_commands = [
        BotCommand(command='start', description='Старт бота'),
        BotCommand(command='help', description='helper'),
        BotCommand(command='mem', description='фотка мема'),
        BotCommand(command='sticker', description='отправка стикеров'),
        BotCommand(command='add_product', description='заполнения нового товара'),
        BotCommand(command='form', description='заполнение анкеты'),
        BotCommand(command='records', description='список записей на пробное занятие'),
        BotCommand(command='products', description='список товаров (JOIN)'),
    ]
    await bot.set_my_commands(bot_commands)


async def on_startup(bot: Bot) -> None:
    create_table()
    await main_db.init_products_db() 
    await set_commands()

    for admin_id in Admin:
        await bot.send_message(chat_id=admin_id, text='Бот включен!')


async def main() -> None:
    dp.include_router(router=commands.commands_router)
    dp.include_router(router=fsm_add_products.router_addproduct)
    dp.include_router(router=fsm.router_fsm)
    dp.include_router(router=echo.router_echo)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())