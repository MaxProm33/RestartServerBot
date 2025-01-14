import os
import logging

import uuid
import json
import discord
from discord.ext import commands
from discord import Option
import requests
from utils.config_loader import load_online_bots_config

SS_TOKEN = os.getenv("SS_TOKEN")                                                    # Получение токена администратора из .env файл

URLS = {                                                                            # Словарь c url серверов
    "Титан": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Фобос": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Фронтир": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Апофис": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Деймос": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Союз-1": "https://ff.deadspace14.net/admin/actions/round/restartnow",
    "Мапперский": "http://185.97.255.17:1225/admin/actions/round/restartnow"

}


SERVER_NAME_MAPPING = {                                                              # Словарь соответствий русских и английских названий серверов
    "Титан": "Titan",
    "Фобос": "Fobos",
    "Фронтир": "Frontier",
    "Деймос": "Deimos",
    "Союз-1": "Souz1",
    "Мапперский": "Mapping",
}

class RestartServerSs14Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = load_online_bots_config("online_servers_bots.json")
        self.server_tokens = {server.name: server.admin_token for server in self.servers} # создание словаря с данными из json файла
        print(self.servers[0].admin_token)


    def restart_server(self, server_name: str, ctx: discord.ApplicationContext) -> requests.Response | None:             # Функция для перезагрузки сервера
        url = URLS.get(server_name)
        english_server_name = SERVER_NAME_MAPPING.get(server_name)
        admin_token = self.server_tokens.get(english_server_name)                       # Получение админ токена для каждого сервера
        if not admin_token:
            logging.error(f"Токен для сервера {server_name} не найден")
            return None


        try:
            actor_guid = str(uuid.UUID(int=ctx.author.id))
        except ValueError:
            self.logger.error(f"Некорректный ID пользователя Discord: {ctx.author.id}. Невозможно преобразовать в GUID.")
            return None
        actor_name = ctx.author.name
        headers = {
            "Authorization": f"SS14Token {admin_token}",
            "Actor": json.dumps({"Guid": actor_guid, "Name": actor_name}),
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, timeout=30)                  # Добавляем таймаут
            logging.info(f"Текст ответа:{response.text}")
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

        result = self.restart_server(server, ctx)

        if result:
            await ctx.respond(f"Сервер {server} успешно перезапущен.")
            logging.info(f"Сервер {server} был успешно перезапущен.")
        else:
            await ctx.respond(f"Не удалось перезапустить сервер {server}. "
                              f"Пожалуйста, обратитесь к администратору.")              # При неудаче логгирование происходит в функции
