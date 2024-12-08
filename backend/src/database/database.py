from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import sys
from dotenv import load_dotenv
import os
import logging

load_dotenv()

DATABASE_RENDER = os.getenv("DB_RENDER")
DATABASE_LOCAL = os.getenv("DB_LOCAL")

if any("pytest" in arg for arg in sys.argv):
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"
else:
    SQLALCHEMY_DATABASE_URL = DATABASE_LOCAL

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_database():
    async with SessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
