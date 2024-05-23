
import os
import sys

# Добавляем корневую директорию в sys.path для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import config

DATABASE_URL = config.DATABASE

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

class AsyncSessionContextManager:
    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def __aenter__(self):
        self.session = self.async_session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

def get_db():
    return AsyncSessionContextManager(SessionLocal)
