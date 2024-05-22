import asyncio
import os
import sys

# Добавляем корневую директорию в sys.path для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.future import select
from db import get_db, User

async def check_users():
    async with get_db() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Chat ID: {user.chat_id}, Hashed Password: {user.hashed_password}")

if __name__ == "__main__":
    asyncio.run(check_users())
