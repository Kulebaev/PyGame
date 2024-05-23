# message_cleaner.py
import asyncio
from aiogram import Bot, types, Router

class MessageCleaner:
    def __init__(self, bot: Bot, router: Router, delay: int = 10):
        self.bot = bot
        self.router = router
        self.delay = delay

    async def delete_message_handler(self, message: types.Message):
        # Sleep for the specified delay time
        await asyncio.sleep(self.delay)
        try:
            # Attempt to delete the message
            await self.bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            # Log or handle the exception if needed
            print(f"Failed to delete message: {e}")
