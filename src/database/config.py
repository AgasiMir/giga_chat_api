from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL
from environs import Env

env = Env()
env.read_env(".env")

url = URL.create(
    drivername=env.str("DB_DRIVER"),
    username=env.str("DB_USER"),
    password=env.str("DB_PASSWORD"),
    host=env.str("DB_HOST"),
    port=env.int("DB_PORT"),
    database=env.str("DB_NAME"),
).render_as_string(hide_password=False)


async_engine = create_async_engine(url)
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass
