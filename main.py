import os
import discord
from settings import DISCORD_TOKEN, CHANNEL_ID
from newsbot import NewsBot

if __name__ == "__main__":
    NEWS_URL = "https://www.oncehuman.game/news/"

    intents = discord.Intents.default()

    client = NewsBot(DISCORD_TOKEN, CHANNEL_ID, NEWS_URL, intents=intents)
    client.run_bot()
