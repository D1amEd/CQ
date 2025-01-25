import asyncio
from services.discord_service import DiscordService
from services.telegram_service import TelegramService

class MessagingService:
    def __init__(self):
        self.discordService= DiscordService()
        self.telegramService= TelegramService()
    
    async def send_message_async(self, message):
        pass
    
    async def send_message(self, message):
        print(message)
        await self.discordService.send_message(message)
        await self.telegramService.send_message(message)
        