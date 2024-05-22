import asyncio
import os
import sys

# Добавляем корневую директорию в sys.path для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect
import config

DATABASE_URL = config.DATABASE

async def check_structure():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(do_inspect)

def do_inspect(conn):
    inspector = inspect(conn)
    tables = inspector.get_table_names()
    if 'chats' in tables:
        columns = inspector.get_columns('chats')
        print(f"Таблица 'chats' существует. Колонки:")
        for column in columns:
            print(f"{column['name']} - {column['type']}")
    else:
        print("Таблица 'chats' не существует.")

asyncio.run(check_structure())
