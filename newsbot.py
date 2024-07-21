import discord
import requests
import asyncio
import json
import os
import settings
from bs4 import BeautifulSoup

logger = settings.logging.getLogger("bot")

class NewsBot(discord.Client):
    def __init__(self, token, channel_id, news_url, check_interval=300, intents=None, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.token = token
        self.channel_id = channel_id
        self.news_url = news_url
        self.check_interval = check_interval
        self.posted_news_file = './NewsBot/cache/posted_news.json'
        self.posted_news = self.load_posted_news()

    def load_posted_news(self):
        if os.path.exists(self.posted_news_file):
            with open(self.posted_news_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_posted_news(self):
        with open(self.posted_news_file, 'w') as file:
            json.dump(self.posted_news, file)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name} ({self.user.id})")
        self.channel = self.get_channel(self.channel_id)

        if self.channel is None:
            logger.error(f"Channel with ID {self.channel_id} not found.")
            return

        self.loop.create_task(self.check_and_post_news())

    async def check_and_post_news(self):
        """ Check for new news and post them to the channel. """
        
        await self.wait_until_ready()
        while not self.is_closed():
            latest_news = self.get_latest_news()
            for news in latest_news:
                title, link, date, description = news
                if title not in self.posted_news:
                    if self.channel:
                        embed = discord.Embed(
                            title=title,
                            url=link,
                            description=description,
                            color=discord.Color.blue()
                        )
                        embed.add_field(name="Date", value=date, inline=True)
                        await self.channel.send(embed=embed)

                        self.posted_news[title] = True
                        self.save_posted_news()
                    else:
                        logger.error(f"Channel with ID {self.channel_id} not found.")
            await asyncio.sleep(self.check_interval)

    def get_latest_news(self):
        """ Get the latest news from the website. """
        
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