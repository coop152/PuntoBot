import discord.ext.commands as commands
import yiffgen


class Generators(commands.Cog):

    # instance members
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="zorn",
                      description="for when you cant decide what kind of zorn youre going to zerk off to")
    async def zorn_generator(self, ctx: commands.Context) -> None:
        zorn = yiffgen.make_zorn()
        if yiffgen.pogg_ing:
            zorn += "\nOMG best ship!!!! i FUCKING LOVE typhlosion x feraligatr its so awesome typhlosion is such an EPIC POWER BOTTOM!!!"
        await ctx.send(zorn)
        if yiffgen.pogg_ing:
            getters = self.bot.get_cog("ImageGetters")
            if getters is None:
                print("The image getting cog isnt loaded, something is broken")
            else:
                # getters will absolutely have this method, the typing is just being a bitch
                await getters.e621(ctx, "typhlosion", "feraligatr", "order:score", "rating:explicit")  # type: ignore
            yiffgen.pogg_ing = False

    @commands.command(name="ship",
                      description="hottest new ship on the internet")
    async def ship_generator(self, ctx: commands.Context) -> None:
        pairing = yiffgen.make_pairing(1, 3)
        if yiffgen.pogg_ing:
            pairing += "\nOMG best ship!!!! i FUCKING LOVE typhlosion x feraligatr its so awesome typhlosion is such an EPIC POWER BOTTOM!!!"
        await ctx.send(pairing)
        if yiffgen.pogg_ing:
            getters = self.bot.get_cog("ImageGetters")
            if getters is None:
                print("The image getting cog isnt loaded, something is broken")
            else:
                # getters will absolutely have this method, the typing is just being a bitch
                await getters.e621(ctx, "typhlosion", "feraligatr", "order:score", "rating:explicit")  # type: ignore
            yiffgen.pogg_ing = False

    @commands.command(name="forcepog",
                      description="aaaaaaaaa",
                      hidden=True)
    async def forcepog(self, ctx: commands.Context):
        yiffgen.pogg_ing = True


# extension setup function
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Generators(bot))
