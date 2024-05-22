import asyncio
from db.db import engine, Base
from db.models import User  # Ensure the model is imported

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы")
    print("Инициализация завершена")

asyncio.run(init_db())
