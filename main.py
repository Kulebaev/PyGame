import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import config
from handlers.start_handler import StartHandler
from handlers.exit_handler import ExitHandler

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация обработчиков
start_router = Router()
exit_router = Router()
StartHandler(start_router)
ExitHandler(exit_router)
dp.include_router(start_router)
dp.include_router(exit_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
