import asyncio
import telegram
from dotenv import load_dotenv
import os
from services.base_messaging_service import BaseMessagingService


class TelegramService(BaseMessagingService):
    def __init__(self):
            load_dotenv()
            self.bot = telegram.Bot(os.getenv("TELEGRAM_BOT_TOKEN"))

    async def send_message(self, message:str):
        async with self.bot:
            await self.bot.send_message(text= message, chat_id=os.getenv("TELEGRAM_DEMO_CHAT_ID"))

    