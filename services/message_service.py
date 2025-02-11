import asyncio
from services.discord_service import DiscordService
from services.telegram_service import TelegramService
from services.smtp_service import GmailSMTPService
import dotenv
import os

class MessagingService:
    def __init__(self):
        dotenv.load_dotenv()
        
        self.discordService= DiscordService()
        self.telegramService= TelegramService()
        print(os.getenv('GMAIL_ADDRESS'))
        self.smtpEmailService= GmailSMTPService(os.getenv('GMAIL_ADDRESS'), os.getenv('GMAIL_PASSWORD'))
    
    async def send_message_shiga(self, message):
        print('-----------------------')
        print(message)
        await self.telegramService.send_shiga(message)
    
    async def send_message(self, message):
        print(message)
        await self.discordService.send_message(message)
        await self.telegramService.send_message(message)
    async def send_message_email_eddie(self, message):
        await self.smtpEmailService.send_email('estebanrco@hotmail.com', 'Bot is failing', message)
        