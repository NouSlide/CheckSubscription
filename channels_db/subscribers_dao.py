from sqlalchemy import insert, select, delete

from channels_db.main_db import async_session_factory
from channels_db.models import ChannelSubscriber


async def save_chan_subs(chan_id, user_id, user_name):
    async with async_session_factory() as session:
        query = select(ChannelSubscriber).where(ChannelSubscriber.channel_id == chan_id).where(ChannelSubscriber.user_id == user_id)
        subs = await session.execute(query)
        if subs.scalar():
            return
        else:
            data_subs = {'user_id': user_id, 'username': user_name, 'channel_id': chan_id}

        insert_data_subs = insert(ChannelSubscriber).values(data_subs)
        await session.execute(insert_data_subs)
        await session.commit()


async def delete_chan_subs(chan_id, user_id):
    async with async_session_factory() as session:
        query = delete(ChannelSubscriber).where(ChannelSubscriber.channel_id == chan_id).where(ChannelSubscriber.user_id == user_id)
        await session.execute(query)
        await session.commit()


async def select_channel_subs(channel_id, user_id):
    async with async_session_factory() as session:
        query = select(ChannelSubscriber.user_id).where(ChannelSubscriber.channel_id == channel_id).where(ChannelSubscriber.user_id == user_id)
        subs = await session.execute(query)
        return subs.scalar()
