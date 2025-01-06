from discord import Option
import discord
import requests
from dotenv import load_dotenv
import os
import logging

from logger import configure_logging

configure_logging(level=logging.INFO)                                               # Подключение логгера, по умолчанию установлен уровень info

load_dotenv()                                                                       # Загрузка .env файла

headers = {                                                                         # Набор данных. Токен администратора находится в .env файле
    "Authorization": f"SS14Token {os.getenv("SS_TOKEN")}",
    "Content-Type": "application/json"
}

@discord.slash_command()
async def restartserver(ctx:discord.ApplicationContext,
                        server:
                        Option(str, description="Выберите сервер, который хотите перезагрузить", choices = ["Титан", "Фобос", "Фронтир", "Апофис", "Деймос"])):       # выдача списка серверов пользователю
    response = ""

    urls = {                                                                        # Словарь c url серверов
        "Титан" : "https://ff.deadspace14.net/admin/actions/round/restartnow",
        "Фобос": "https://ff.deadspace14.net/admin/actions/round/restartnow",
        "Фронтир": "https://ff.deadspace14.net/admin/actions/round/restartnow",
        "Апофис": "https://ff.deadspace14.net/admin/actions/round/restartnow",
        "Деймос": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    }

    response = requests.post(urls[server], headers=headers)

    # Обработка ответа
    if response.status_code == 200:                                             # Проверка ответа от сервера
        await ctx.respond(f"{server} успешно перезапущен.")
        logging.info(f"{server} был успешно перезапущен")
    else:
       await ctx.respond(f"К сожалалению не удалось перезапустить {server}. Ошибка: {response.status_code} - {response.text}")
       logging.info(f"К сожалалению не удалось перезапустить {server}. Ошибка: {response.status_code} - {response.text}")

def setup(bot: discord.Bot):                                                    # Загрузка кога
    bot.add_application_command(restartserver)
