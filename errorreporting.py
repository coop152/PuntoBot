from typing import Optional
import discord.ext.commands as commands
from discord.ext.commands import CommandNotFound
from datetime import datetime
from traceback import print_exception, format_exception


class ErrorReporting(commands.Cog):

    # instance members
    bot: commands.Bot
    last_exception: Optional[Exception]
    exception_time: Optional[datetime]

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.last_exception = None
        self.exception_time = None

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, ex: Exception):
        if type(ex) is CommandNotFound and ctx.message is not None:
            bad_command = ctx.message.content.split(" ")[0]
            await ctx.send(f"`{bad_command}` is not a command. Check `{self.bot.command_prefix}help` for a list of all commands.")
        else:
            print_exception(type(ex), ex, ex.__traceback__)
            self.last_exception = ex
            self.exception_time = datetime.now()
            print(f"Exception saved for {self.bot.command_prefix}lasterror")
            await ctx.send(f"That command caused an error! See `{self.bot.command_prefix}lasterror` for details.")

    @commands.command(name="lasterror", description="See the traceback of the last error.")
    async def last_error(self, ctx: commands.Context):
        if self.last_exception is None or self.exception_time is None:
            await ctx.send("There hasn't been an unhandled exception yet.")
        else:
            ex = self.last_exception
            text = f"Exception from {self.exception_time}:"
            text = "".join(format_exception(type(ex), ex, ex.__traceback__))
            text = f"```py\n{text}\n```"
            await ctx.send(text)

    # @commands.command(name="debugerror", description="Purposefully create a ValueError. For debugging.")
    # async def error_on_purpose(self, ctx):
    #     x = int("wrong")


# extension setup function
def setup(bot: commands.Bot) -> None:
    bot.add_cog(ErrorReporting(bot))
