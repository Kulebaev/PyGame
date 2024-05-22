from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from sqlalchemy.future import select
from db import get_db, User, Chat

class Form(StatesGroup):
    username = State()
    password = State()

class StartHandler:
    def __init__(self, router: Router):
        self.router = router
        self.router.message.register(self.start_handler, Command("start"))
        self.router.message.register(self.process_username, Form.username)
        self.router.message.register(self.process_password, Form.password)

    async def start_handler(self, message: Message, state: FSMContext):
        async with get_db() as db:
            chat_id = str(message.chat.id)
            chat = await db.execute(select(Chat).filter(Chat.chat_id == chat_id))
            chat = chat.scalars().first()
            if not chat:
                chat = Chat(chat_id=chat_id)
                db.add(chat)
                await db.commit()

            user_query = select(User).join(User.chat).where(Chat.chat_id == chat_id, User.username == message.from_user.username)
            user_result = await db.execute(user_query)
            user = user_result.scalars().first()

            if user:
                await message.answer("Вы уже вошли.")
                return
            await message.answer("Привет! Пожалуйста, введите ваше имя пользователя.")
            await state.set_state(Form.username)

    async def process_username(self, message: types.Message, state: FSMContext):
        async with get_db() as db:
            username = message.text
            user_query = select(User).where(User.username == username)
            user_result = await db.execute(user_query)
            user = user_result.scalars().first()
            
            if user:
                await message.answer("Это имя пользователя уже существует, пожалуйста, введите другое имя.")
                return
            
            await state.update_data(username=username)
            await message.answer("Пожалуйста, введите ваш пароль.")
            await state.set_state(Form.password)

    async def process_password(self, message: types.Message, state: FSMContext):
        await state.update_data(password=message.text)
        data = await state.get_data()

        username = data['username']

        hashed_password = data['password']  # Здесь вы можете захешировать пароль перед сохранением

        async with get_db() as db:
            chat_id = str(message.chat.id)
            chat = await db.execute(select(Chat).filter(Chat.chat_id == chat_id))
            chat = chat.scalars().first()
            if not chat:
                chat = Chat(chat_id=chat_id)
                db.add(chat)
                await db.commit()
                chat_id_in_db = chat.id
            else:
                chat_id_in_db = chat.id
            user = User(chat_id=chat_id_in_db, username=username, hashed_password=hashed_password)
            db.add(user)
            await db.commit()

        await message.answer(f"Спасибо за регистрацию!\nВаш логин: {username}\nВаш пароль: {hashed_password}")

        await state.clear()
