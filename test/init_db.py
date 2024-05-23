import asyncio
import os
import sys

# Добавляем корневую директорию в sys.path для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.db import engine, Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())
