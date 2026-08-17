from os import getenv
from typing import Annotated, AsyncGenerator

from dotenv import load_dotenv

from fastapi import Depends

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker


load_dotenv()

user = getenv("POSTGRES_USER")
password = getenv("POSTGRES_PASSWORD")
host = getenv("POSTGRES_HOST")

postgres_db_name = "main"
postgres_connection_url = (
    f"postgresql+psycopg://{user}:{password}@{host}:5432/{postgres_db_name}"
)

engine = create_async_engine(postgres_connection_url)


session_pool = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_pool() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
