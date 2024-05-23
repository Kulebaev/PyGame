
import os
import sys

# Добавляем корневую директорию в sys.path для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# handlers/start_handler.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from sqlalchemy.future import select
from db import get_db, User, Chat
import config
from db.utils import DatabaseUtils

class StartHandler:
    def __init__(self, router: Router):
        self.router = router
        self.router.message.register(self.start_handler, Command("start"))

    async def start_handler(self, message: Message):
        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            chat_id = str(message.chat.id)
            user = await db_utils.get_user_by_chat_id(chat_id)
            if user:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Запустить приложение", web_app=WebAppInfo(url=config.SITE_URL))]
                ])
                await message.answer("Вы уже авторизованы. Доступны следующие команды:", reply_markup=keyboard)
            else:
                await message.answer("Привет! Вы можете:\n/register - Зарегистрироваться\n/auth - Авторизоваться")
