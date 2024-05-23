# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
import config
from handlers.start_handler import StartHandler
from handlers.exit_handler import ExitHandler
from handlers.register_handler import RegisterHandler
from handlers.auth_handler import AuthHandler
from handlers.app_handler import AppHandler

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создание роутеров
start_router = Router()
exit_router = Router()
register_router = Router()
auth_router = Router()
app_router = Router()

# Регистрация обработчиков
StartHandler(start_router)
ExitHandler(exit_router)
RegisterHandler(register_router)
AuthHandler(auth_router)
AppHandler(app_router)

# Включение роутеров в диспетчер
dp.include_router(start_router)
dp.include_router(exit_router)
dp.include_router(register_router)
dp.include_router(auth_router)
dp.include_router(app_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
