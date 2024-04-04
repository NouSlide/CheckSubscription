from dotenv import load_dotenv, find_dotenv
import os

import asyncio
from aiogram import Bot, Dispatcher

from code_bot.handlers_user import private_router

from channels_db.create_tables import create_tables


load_dotenv(find_dotenv())

API_TOKEN = os.getenv('BOT_TOKEN')


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.include_router(private_router)

    await create_tables()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
