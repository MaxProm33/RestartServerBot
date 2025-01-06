import os
import discord
from dotenv import load_dotenv
import logging

from logger import configure_logging

configure_logging(level=logging.INFO)

load_dotenv()

bot = discord.Bot(debug_guilds=[1324373556473364490])

@bot.event
async def on_ready():
    print("Бот успешно запущен и готов к работе")
    logging.info("Бот успешно запущен")


bot.load_extension("cogs.restart")                                                       # загрузка кога перезагрузки
bot.run(os.getenv("BOT_TOKEN"))
