import os
import logging

import discord
from discord.ext import commands
from discord import Option
import requests
from dotenv import load_dotenv
from cogs.ss14_admin_manager.logger import configure_logging

configure_logging(level=logging.INFO)                                               # Подключение логгера, по умолчанию установлен уровень info
load_dotenv()                                                                       # Загрузка .env файла

SS_TOKEN = os.getenv("SS_TOKEN")                                                    # Получение токена администратора из .env файл

URLS = {                                                                            # Словарь c url серверов
    "Титан": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Фобос": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Фронтир": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Апофис": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Деймос": "https://ff.deadspace14.net/admin/actions/round/restartnow",
}

class RestartServerSs14Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def restart_server(self, server_name: str) -> requests.Response | None:             # Функция для перезагрузки сервера
        url = URLS.get(server_name)
        headers = {
            "Authorization": f"SS14Token {SS_TOKEN}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, timeout=10)                  # Добавляем таймаут
            response.raise_for_status()                                                 # Вызывает исключение для HTTP ошибок (4xx, 5xx)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при перезапуске сервера {server_name}: {e}")
            return None

    @discord.slash_command(name="restartserver", description="Перезагружает указанный сервер.")# Команда для перезагрузки сервера
    async def restart_server_command(self, ctx: discord.ApplicationContext,
                                     server: Option(str, description="Выберите сервер для перезагрузки.",
                                                   choices=list(URLS.keys()))):

        await ctx.defer()                                                               # Откладываем ответ для возможности задержки со стороны сервера

        result = self.restart_server(server)

        if result:
            await ctx.respond(f"Сервер {server} успешно перезапущен.")
            logging.info(f"Сервер {server} был успешно перезапущен.")
        else:
            await ctx.respond(f"Не удалось перезапустить сервер {server}. "
                              f"Пожалуйста, обратитесь к администратору.")              # При неудаче логгирование происходит в функции

def setup(bot):                                                                         # Загрузка кога
    bot.add_cog(RestartServerSs14Cog(bot))