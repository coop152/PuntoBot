from typing import Union
import discord.ext.commands as commands
from discord import Member, Message, Embed
import pokebase

# TODO: buttons and start doing the actual game part
# TODO: remember to start using the db


class SmashOrPass(commands.Cog):

    bot: commands.Bot
    active_games: dict[int, int]  # user ID: message ID

    def __init__(self, bot) -> None:
        self.bot = bot
        self.active_games = {}

    # @profile
    def get_deets(self, name_or_id: Union[str, int]) -> Embed:
        pokemon = pokebase.pokemon(name_or_id)
        fixed_desc: str = [
            x for x in pokemon.species.flavor_text_entries if x.language.name == "en"][0].flavor_text
        fixed_desc = fixed_desc.replace(u"\f", u"\n") \
            .replace(u'\u00ad\n', u'') \
            .replace(u'\u00ad', u'') \
            .replace(u' -\n', u' - ') \
            .replace(u'-\n', u'-') \
            .replace(u'\n', u' ')
        return Embed.from_dict({
            "type": "rich",
            "title": "Smash or Pass?",
            "description": f"#{pokemon.id} - {pokemon.name.capitalize()}",
            "color": 0xFF0000,
            "image": {
                "url": pokemon.sprites.other.__getattribute__("official-artwork").front_default,
                "height": 0,
                "width": 0
            },
            "fields": [{
                "name": "Description:",
                "value": fixed_desc
            }]
        })

    @commands.command(name="pokesmash",
                      description="Start a session of Pokemon smash or pass.")
    async def start_game(self, ctx: commands.Context, *args: str) -> None:
        if ctx.message.author.id in self.active_games.keys():
            await ctx.send("You already have a game going!",
                           reference=await ctx.fetch_message(self.active_games[ctx.message.author.id]))
            return
        game_msg: Message = await ctx.send(f"{ctx.message.author}'s Game")
        self.active_games[ctx.message.author.id] = game_msg.id
        await self.update_game(game_msg)

    @commands.command(name="pokesmashstop")
    async def stop_game(self, ctx: commands.Context, *args: str) -> None:
        if ctx.message.author.id not in self.active_games.keys():
            await ctx.send("You don't have a game running!")
            return
        self.active_games.pop(ctx.message.author.id)
        await ctx.send("Stopped your game.")

    pokenum = 4

    async def update_game(self, game_msg: Message) -> None:
        new_embed = self.get_deets(self.pokenum)
        self.pokenum += 1
        await game_msg.edit(embed=new_embed)

    @commands.command()
    async def tempupdgame(self, ctx: commands.Context) -> None:
        await self.update_game(await ctx.fetch_message(self.active_games[ctx.author.id]))


# extension setup function
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SmashOrPass(bot))
