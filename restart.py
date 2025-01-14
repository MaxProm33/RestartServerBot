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
        self.server_tokens = {server.name: server.admin_token for server in self.servers} # Создание словаря с данными из json файла по типу: "имя сервера: админ токен"
        self.server_ips = {server.name: server.ip for server in self.servers}             # Создание словаря с данными из json файла по типу: "имя сервера: ip сервера"

    def restart_server(self, server_name: str, ctx: discord.ApplicationContext) -> requests.Response | None:             # Функция для перезагрузки сервера
        english_server_name = SERVER_NAME_MAPPING.get(server_name)

        ip_port = self.server_ips.get(english_server_name)

        if not ip_port:
            self.logger.error(f"IP:порт для сервера {server_name} не найден")
            return None

        url = f"http://{ip_port}/admin/actions/round/restartnow"                        # ip : порт из json файла

        admin_token = self.server_tokens.get(english_server_name)

        if not admin_token:
            self.logger.error(f"Токен для сервера {server_name} не найден")
            return None

        admin_token = self.server_tokens.get(english_server_name)                       # Получение админ токена для каждого сервера

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
                                                   choices=list(SERVER_NAME_MAPPING.keys()))):

        await ctx.defer()                                                               # Откладываем ответ для возможности задержки со стороны сервера

        result = self.restart_server(server, ctx)

        if result:
            await ctx.respond(f"Сервер {server} успешно перезапущен.")
            logging.info(f"Сервер {server} был успешно перезапущен пользователем {ctx.author.name}.")
        else:
            await ctx.respond(f"Не удалось перезапустить сервер {server}. "
                              f"Пожалуйста, обратитесь к администратору.")              # При неудаче логгирование происходит в функции
