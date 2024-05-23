# db/utils.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import User, Chat

class DatabaseUtils:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_chat(self, chat_id: str):
        chat = await self.db.execute(select(Chat).filter(Chat.chat_id == chat_id))
        chat = chat.scalars().first()
        if not chat:
            chat = Chat(chat_id=chat_id)
            self.db.add(chat)
            await self.db.commit()
            await self.db.refresh(chat)
        return chat

    async def user_exists(self, username: str):
        user_query = select(User).where(User.username == username)
        user_result = await self.db.execute(user_query)
        return user_result.scalars().first()

    async def get_user_by_chat_id(self, chat_id: str):
        chat = await self.db.execute(select(Chat).filter(Chat.chat_id == chat_id))
        chat = chat.scalars().first()
        if not chat:
            return None
        user_query = select(User).where(User.chat_id == chat.id)
        user_result = await self.db.execute(user_query)
        return user_result.scalars().first()
