from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.future import select
from db import get_db, User, Chat
from db.utils import DatabaseUtils

class ExitHandler:
    def __init__(self, router: Router):
        self.router = router
        self.router.message.register(self.exit_handler, Command("exit"))

    async def exit_handler(self, message: Message):
        async with get_db() as db:
            chat_id = str(message.chat.id)
            user_query = select(User).join(User.chat).where(Chat.chat_id == chat_id)
            user_result = await db.execute(user_query)
            user = user_result.scalars().first()
            
            if user:
                user.chat_id = None
                await db.commit()
                await message.answer("Вы вышли из чата.")
            else:
                await message.answer("Вы не зарегистрированы.")
