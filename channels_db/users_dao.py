from sqlalchemy import insert, select

from channels_db.main_db import async_session_factory
from channels_db.models import TelegramUser


async def add_user(full_name, user_id, username):
    async with async_session_factory() as session:
        query = select(TelegramUser).where(TelegramUser.user_id == user_id)
        user = await session.execute(query)
        if user.scalar():
            return
        else:
            data_user = {'user_id': user_id, 'full_name': full_name, 'username': username}

        insert_data_user = insert(TelegramUser).values(data_user)
        await session.execute(insert_data_user)
        await session.commit()


async def select_user():
    async with async_session_factory() as session:
        query = select(TelegramUser.user_id)
        user = await session.execute(query)
        return user.scalars().all()
