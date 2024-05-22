import asyncio
import os
import sys

# Добавляем корневую директорию в sys.path для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from db import User

DATABASE_URL = config.DATABASE

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def clear_users():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(delete(User))
            await session.commit()
        print("Таблица 'users' очищена.")

if __name__ == "__main__":
    asyncio.run(clear_users())
