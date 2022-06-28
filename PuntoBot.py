from os import getenv

from discord.ext.commands import Bot
from dotenv import load_dotenv

PREFIX = "=="
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

bot = Bot(command_prefix=PREFIX)
bot.load_extension("setup")
bot.load_extension("errorreporting")
bot.load_extension("image_getters")
bot.load_extension("generators")
bot.run(TOKEN)
