import asyncio
import telegram
from dotenv import load_dotenv
import os
from services.base_messaging_service import BaseMessagingService
from telegram.request import HTTPXRequest


class TelegramService(BaseMessagingService):
    def __init__(self):
            load_dotenv()
            request = HTTPXRequest(connection_pool_size=30)
            self.bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"), request=request)
            # Limit concurrent sends to 10 at a time
            self._semaphore = asyncio.Semaphore(20)

    async def send_message(self, message:str):
        async with self.bot:
            await self.bot.send_message(text= message, chat_id=os.getenv("TELEGRAM_DEMO_CHAT_ID"))

    async def send_shiga(self, message:str):
        async with self.bot:
            await self.bot.send_message(text= message, chat_id=os.getenv("TELEGRAM_SHIGA_CHAT_ID"))
