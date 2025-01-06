import os
import discord
from dotenv import load_dotenv
import logging

from logger import configure_logging

configure_logging(level=logging.INFO)                                                   # Подключение логгера, по умолчанию установлен уровень info

load_dotenv()                                                                           # Загрузка .env файла

bot = discord.Bot()

@bot.event                                                                              # Уведомление о том, что дискорд бот запущен
async def on_ready():
    logging.info("Бот успешно запущен")


bot.load_extension("cogs.restart")                                                       # Загрузка кога перезагрузки
bot.run(os.getenv("BOT_TOKEN"))                                                          # Запрос токена бота дискорда из .env файла
