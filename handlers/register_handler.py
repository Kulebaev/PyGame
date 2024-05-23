from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from db import get_db, User
from utils.password import hash_password
from db.utils import DatabaseUtils
from utils.states import Form

class RegisterHandler:
    def __init__(self, router: Router):
        self.router = router
        self.router.message.register(self.register_handler, Command("register"))
        self.router.message.register(self.process_username, Form.username)
        self.router.message.register(self.process_email, Form.email)
        self.router.message.register(self.process_password, Form.password)

    async def register_handler(self, message: Message, state: FSMContext):
        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            chat_id = str(message.chat.id)
            chat = await db_utils.get_or_create_chat(chat_id)

            # Check if a user with the current chat_id exists
            user_query = select(User).where(User.chat_id == chat.id)
            user_result = await db.execute(user_query)
            user = user_result.scalars().first()

            if user:
                await message.answer("Вы уже зарегистрированы и вошли в систему.")
                return
            await message.answer("Пожалуйста, введите ваше имя пользователя.")
            await state.set_state(Form.username)

    async def process_username(self, message: types.Message, state: FSMContext):
        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            username = message.text
            user = await db_utils.user_exists(username)
            
            if user:
                await message.answer("Это имя пользователя уже существует, пожалуйста, введите другое имя.")
                return
            
            await state.update_data(username=username)
            await message.answer("Пожалуйста, введите вашу электронную почту.")
            await state.set_state(Form.email)

    async def process_email(self, message: types.Message, state: FSMContext):
        await state.update_data(email=message.text)
        await message.answer("Пожалуйста, введите ваш пароль.")
        await state.set_state(Form.password)

    async def process_password(self, message: types.Message, state: FSMContext):
        await state.update_data(password=message.text)
        data = await state.get_data()

        username = data['username']
        email = data['email']
        password = data['password']
        hashed_password = hash_password(password)

        async with get_db() as db:
            db_utils = DatabaseUtils(db)
            chat_id = str(message.chat.id)
            chat = await db_utils.get_or_create_chat(chat_id)
            chat_id_in_db = chat.id

            user = User(chat_id=chat_id_in_db, username=username, email=email, hashed_password=hashed_password)
            db.add(user)

            try:
                await db.commit()
                await message.answer(f"Спасибо за регистрацию!\nВаш логин: {username}\nВаш email: {email}\nВаш пароль: {password}")
                await state.clear()
            except IntegrityError:
                await db.rollback()
                await message.answer("Имя пользователя уже существует, пожалуйста, введите другое имя.")
                await state.set_state(Form.username)
