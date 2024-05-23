# auth_handler.py
from aiogram import Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from db import get_db, User
from utils.password import verify_password
from aiogram.filters import Command
from db.utils import DatabaseUtils
from utils.states import Form

class AuthHandler:
    def __init__(self, router: Router):
        self.router = router
        self.router.message.register(self.auth_handler, Command("auth"))
        self.router.message.register(self.process_username_auth, Form.username_auth)
        self.router.message.register(self.process_password_auth, Form.password_auth)

    async def auth_handler(self, message: Message, state: FSMContext):
        await message.answer("Пожалуйста, введите ваше имя пользователя.")
        await state.set_state(Form.username_auth)

    async def process_username_auth(self, message: types.Message, state: FSMContext):
        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            username = message.text
            user = await db_utils.user_exists(username)

            if not user:
                await message.answer("Пользователь с таким именем не найден, пожалуйста, введите другое имя.")
                return

            await state.update_data(username=username)
            await message.answer("Пожалуйста, введите ваш пароль.")
            await state.set_state(Form.password_auth)

    async def process_password_auth(self, message: types.Message, state: FSMContext):
        await state.update_data(password=message.text)
        data = await state.get_data()

        username = data['username']
        password = data['password']

        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            user = await db_utils.user_exists(username)

            if user and verify_password(password, user.hashed_password):
                chat_id = str(message.chat.id)
                chat = await db_utils.get_or_create_chat(chat_id)
                user.chat_id = chat.id
                await db.commit()
                await message.answer("Вы успешно авторизовались!")
                await state.clear()
            else:
                await message.answer("Неверное имя пользователя или пароль. Введите имя пользователя ещё раз.")
                await state.set_state(Form.username_auth)
