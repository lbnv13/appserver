# import os
from sqlalchemy.ext.asyncio import AsyncSession,  create_async_engine
from sqlalchemy.orm import sessionmaker

# APP SETTINGS


# AD
# ldap3 settings
servername = 'vmz.local'
domain = 'vmz'
SearchBase = 'DC=vmz,DC=local'

# DB
# postgres settings
DB_HOST = '192.168.105.12'
DB_PORT = '5432'
DB_NAME = 'WorkSpace'
DB_USER = 'postgres'
DB_PASS = 'sqladmin'


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
