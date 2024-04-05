import asyncio
from aiogram import Bot, Dispatcher

from code_bot.handlers_user import private_router

from channels_db.create_tables import create_tables


async def main():
    API_TOKEN = '123456789' # Токен бота
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.include_router(private_router)

    await create_tables()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
