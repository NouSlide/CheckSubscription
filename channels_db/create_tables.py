from channels_db.main_db import engine
from channels_db.models import Base


async def create_tables():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all) # Здесь таблицы удаляются вместе со всеми данными
        await con.run_sync(Base.metadata.create_all) # Здесь они заново создаются