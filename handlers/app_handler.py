# handlers/app_handler.py
from aiogram import Router, types
from aiogram.types import Message
from db.utils import DatabaseUtils
from aiogram.filters import Command
from db import get_db
import subprocess

class AppHandler:
    def __init__(self, router: Router):
        self.router = router
        self.router.message.register(self.run_app_handler, Command("runapp"))

    async def run_app_handler(self, message: Message):
        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            chat_id = str(message.chat.id)
            user = await db_utils.get_user_by_chat_id(chat_id)
            if user:
                subprocess.run(["python", "app/test_app.py"])
                await message.answer("Приложение запущено!")
            else:
                await message.answer("Вы не авторизованы.")
