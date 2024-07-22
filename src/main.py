import os
import discord
from settings import DISCORD_TOKEN
from botmanager import BotManager

if __name__ == "__main__":
    intents = discord.Intents.default()
    bot = BotManager(command_prefix="!", intents=intents)
    bot.run(DISCORD_TOKEN)
