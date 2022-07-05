import discord.ext.commands as commands

class SmashOrPass(commands.Cog):

    bot: commands.Bot

    def __init__(self, bot) -> None:
        self.bot = bot

# extension setup function
def setup(bot: commands.Bot) -> None:
    bot.add_cog(SmashOrPass(bot))

