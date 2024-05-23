# exit_handler.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from db import get_db, User, Chat
from db.utils import DatabaseUtils

class ExitHandler:
    def __init__(self, router: Router):
        self.router = router
        self.router.message.register(self.exit_handler, Command("exit"))

    async def exit_handler(self, message: Message, state: FSMContext):
        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            chat_id = str(message.chat.id)
            user_query = select(User).join(User.chat).where(Chat.chat_id == chat_id)
            user_result = await db.execute(user_query)
            user = user_result.scalars().first()
            
            await state.clear()  # Очистка состояния

            if user:
                user.chat_id = None
                await db.commit()
                await message.answer("Вы вышли.")
                return
            
            await message.answer("Команда /exit выполнена.")
