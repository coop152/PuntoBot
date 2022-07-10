from os import getenv
from typing import Optional, Union
import discord.ext.commands as commands
from discord import Member, Message, Embed
from dotenv import load_dotenv
from simplepokewrapper import PokeWrapper

# TODO: buttons and start doing the actual game part
# TODO: remember to start using the db


class SmashOrPass(commands.Cog):

    bot: commands.Bot
    active_games: dict[int, int]  # user ID: message ID

    def __init__(self, bot, db_url) -> None:
        self.bot = bot
        self.active_games = {}
        self.api = PokeWrapper(db_url)

    # @profile
    def get_deets(self, name_or_id: Union[str, int]) -> Optional[Embed]:
        resp = self.api.all_details(name_or_id)
        if resp is None:
            return None
        fixed_desc = resp['pokedex'].replace(u"\f", u"\n") \
            .replace(u'\u00ad\n', u'') \
            .replace(u'\u00ad', u'') \
            .replace(u' -\n', u' - ') \
            .replace(u'-\n', u'-') \
            .replace(u'\n', u' ')
        return Embed.from_dict({
            "type": "rich",
            "title": "Smash or Pass?",
            "description": f"#{resp['id']} - {resp['name']}",
            "color": 0xFF0000,
            "image": {
                "url": resp['sprite'],
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

    async def update_game(self, game_msg: Message) -> bool:
        new_embed = self.get_deets(self.pokenum)
        if new_embed is None:
            await game_msg.edit(content="The API isn't working right now!")
            return False
        else:
            self.pokenum += 1
            await game_msg.edit(embed=new_embed)
            return True

    @commands.command()
    async def tempupdgame(self, ctx: commands.Context) -> None:
        success = await self.update_game(await ctx.fetch_message(self.active_games[ctx.author.id]))
        if not success:
            await self.stop_game(ctx)


# extension setup function
async def setup(bot: commands.Bot) -> None:
    load_dotenv()
    db_url = getenv("DATABASE_URL")
    await bot.add_cog(SmashOrPass(bot, db_url))
