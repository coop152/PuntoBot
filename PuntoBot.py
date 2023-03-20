from os import getenv
from discord import Intents

from discord.ext.commands import Bot
from dotenv import load_dotenv

PREFIX = "??"
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')


class PuntoBot(Bot):
    async def setup_hook(self) -> None:
        await bot.load_extension("setup")
        await bot.load_extension("errorreporting")
        await bot.load_extension("image_getters")
        await bot.load_extension("generators")
        await bot.load_extension("ai_chatbot")
        await super().setup_hook()


if TOKEN is None:
    print("The token isn't in .env or the environment variables.\nAdd it with the name 'DISCORD_TOKEN'.")
else:
    # idk how intents work LMAO!!!!!
    bot = PuntoBot(command_prefix=PREFIX, intents=Intents.all())
    bot.run(TOKEN)
