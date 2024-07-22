import discord
import settings

from discord.ext import commands
from newsbot import NewsBot
from serversettings import ServerSettings

logger = settings.logging.getLogger("bot")

class BotManager(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        self.server_settings = ServerSettings()
        self.add_cog(NewsBot(self, self.server_settings))

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name} ({self.user.id})")