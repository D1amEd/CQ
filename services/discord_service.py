import asyncio
import os
import pyperclip
import discord
import asyncio
import time
import aiohttp 
from dotenv import load_dotenv
from services.base_messaging_service import BaseMessagingService
class DiscordService(BaseMessagingService):
    def __init__(self, token=None, guild_id=None, channel_id=None):
        load_dotenv()
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.webhooks = os.getenv("WEBHOOK_URLS", "").split(",")
        self.index_lock = asyncio.Lock()
        self.current_webhook_index = 0

        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')
            guild = self.client.get_guild(self.guild_id)
            if guild:
                print(f"Connected to guild: {guild.name}")
            else:
                print(f"Could not find guild with ID {self.guild_id}")
          
    async def send_message(self, message: str):
        async with self.index_lock:
            webhook_url = self.webhooks[self.current_webhook_index]
            self.current_webhook_index = (self.current_webhook_index + 1) % len(self.webhooks)

            # Send the message through the selected webhook
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json={"content": message}) as response:
                if response.status != 204:  # 204 is Discord's "no content" response for successful requests
                    print(f"Failed to send message: {response.status}")

    def start_bot(self):
        self.client.run(self.token)
    
