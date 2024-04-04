from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())

DB_NAME = f'sqlite+aiosqlite:///{os.getenv("DB_NAME")}'


engine = create_async_engine(url=DB_NAME, echo=True)

async_session_factory = async_sessionmaker(engine)
