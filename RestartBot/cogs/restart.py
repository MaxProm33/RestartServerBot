from discord import Option
import discord
import requests
from dotenv import load_dotenv
import os
import logging

from logger import configure_logging

configure_logging(level=logging.INFO)                                               # загрузка люггера

load_dotenv()                                                                       # загрузка .env файла

#Ссылки на серверы, которые нужно перезагрузить
titan_url = "https://ff.deadspace14.net/admin/actions/round/restartnow"             #Ссылка для перезагрузки титана
phobos_url = "https://ff.deadspace14.net/admin/actions/round/restartnow"            #Ссылка для перезагрузки фобоса
frontier_url = "https://ff.deadspace14.net/admin/actions/round/restartnow"          #Ссылка для перезагрузки фронтира
apophis_url = "https://ff.deadspace14.net/admin/actions/round/restartnow"           #Ссылка для перезагрузки апофиса
deimos_url = "https://ff.deadspace14.net/admin/actions/round/restartnow"            #Ссылка для перезагрузки деймоса


headers = {                                                                         #Набор данных. Токен администратора находится в .env файле
    "Authorization": f"SS14Token {os.getenv("SS_TOKEN")}",
    "Content-Type": "application/json"
}

@discord.slash_command()
async def restartserver(ctx:discord.ApplicationContext,
                        server:
                        Option(str, description="Выберите сервер, который хотите перезагрузить", choices = ["Титан", "Фобос", "Фронтир", "Апофис", "Деймос"])):       # выдача списка серверов пользователю
    response = ""
    match server:                                                               #Выполнение запроса в зависимости от выбранного сервера для перезагрузки
        case "Титан":
            response = requests.post(titan_url, headers=headers)

        case "Фобос":
            response = requests.post(phobos_url, headers=headers)

        case "Фронтир":
            response = requests.post(frontier_url, headers=headers)

        case "Апофис":
            response = requests.post(apophis_url, headers=headers)

        case "Деймос":
            response = requests.post(deimos_url, headers=headers)

    # Обработка ответа
    if response.status_code == 200:                                             #Проверка ответа от сервера
        await ctx.respond(f"{server} успешно перезапущен.")
        logging.info(f"{server} был успешно перезапущен")
    else:
       await ctx.respond(f"К сожалалению не удалось перезапустить {server}. Ошибка: {response.status_code} - {response.text}")
       logging.info(f"К сожалалению не удалось перезапустить {server}. Ошибка: {response.status_code} - {response.text}")

def setup(bot: discord.Bot):
    bot.add_application_command(restartserver)


