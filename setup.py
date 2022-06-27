import discord.ext.commands as commands
from discord import Embed, Game


class Setup(commands.Cog):

    # instance members
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="help",
                      description="Displays this list of commands.")
    async def help(self, ctx: commands.Context) -> None:
        help_message = Embed(title="Help", color=0xFF8000)
        help_message.set_author(name="Jeffrey Epstein",
                                url="https://google621.neocities.org")  # type: ignore
        help_message.set_thumbnail(
            url="https://pbs.twimg.com/profile_images/1315716250706882563/Z1eDpiVY_400x400.jpg")
        for command in self.bot.commands:
            if not command.hidden:
                help_message.add_field(name=self.bot.command_prefix + command.name,
                                       value=command.description if command.description else "[no description added]",
                                       inline=False)
        await ctx.send(embed=help_message)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Trying to set presence... ")
        await self.bot.change_presence(activity=Game(name="gaming, like a boss"))
        if self.bot.user:  # if bot has a user account
            print("Logged in as " + self.bot.user.name)
        else:
            print("The bot doesn't have a user account. Something has gone wrong.")


# extension setup function
def setup(bot: commands.Bot) -> None:
    bot.remove_command("help")
    bot.add_cog(Setup(bot))
