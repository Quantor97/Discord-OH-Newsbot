import discord
import requests
import asyncio
import json
import os
import settings
from serversettings import ServerSettings

from bs4 import BeautifulSoup
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class NewsBot(commands.Cog):
    def __init__(self, bot : discord.Client, server_settings : ServerSettings):
        self.bot = bot
        self.server_settings = server_settings
        self.news_url = "https://www.oncehuman.game/news/"
        self.check_interval = 300
        self.posted_news_file = './cache/posted_news.json'
        self.posted_news = self.load_posted_news()
        
        if not ( self.bot or self.server_settings ):
            raise ValueError("Bot and ServerSettings must be provided.")
        
        bot.loop.create_task(self.check_and_post_news())

    def load_posted_news(self):
        if os.path.exists(self.posted_news_file):
            with open(self.posted_news_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_posted_news(self):
        with open(self.posted_news_file, 'w') as file:
            json.dump(self.posted_news, file)

    @commands.command(name='setchannel')
    @commands.has_any_role('mods')
    async def set_channel(self, ctx, channel: discord.TextChannel):
        if not channel:
            await ctx.send('Invalid channel')
            return
        
        self.server_settings.set_channel(ctx.guild.id, channel.id)
        await ctx.send(f'Notifications channel set to {channel.mention}')

    async def send_news(self, channel):
        if not channel:
            return

        latest_news = self.get_latest_news()

        for news in latest_news:
            title, link, date, description = news
            if title not in self.posted_news:
                embed = discord.Embed(
                    title=title,
                    url=link,
                    description=description,
                    color=discord.Color.blue()
                )
                embed.add_field(name="Date", value=date, inline=True)
                await channel.send(embed=embed)

                self.posted_news[title] = True
                self.save_posted_news()
        

    async def check_and_post_news(self):
        """ Check for new news and post them to the channel. """

        logger.info("Checking for new news...")

        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for guild in self.bot.guilds:
                channel_id = self.server_settings.get_channel(guild.id)
                if channel_id:
                    channel = self.bot.get_channel(channel_id)
                    await self.send_news(channel)
                else:
                    logger.warning(f"Channel not set for guild {guild.name}")

            await asyncio.sleep(self.check_interval)
        

    def get_latest_news(self):
        """ Get the latest news from the website. """

        logger.info("Getting latest news...")
        
        response = requests.get(self.news_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('div', class_='newsinfo')
        latest_news = []

        for article in articles:
            title_tag = article.find('h3')
            title = title_tag.text.strip() if title_tag.text.strip() else title_tag.get('title')
            description = article.find('div', class_='text').text.strip()
            date = article.find_next_sibling('div', class_='newsfot').find('div', class_='time').text
            link = article.find_next_sibling('div', class_='newsfot').find('div', class_='btn-more').get('data-link')
            latest_news.append((title, link, date, description))

        return latest_news

    def run_bot(self):
        self.run(self.token)