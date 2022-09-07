from dataclasses import dataclass, field
from os import getenv
from typing import Optional, Union
import discord.ext.commands as commands
import discord
from dotenv import load_dotenv
from zmq import Message
from simplepokewrapper import PokeWrapper

# TODO: buttons and start doing the actual game part
# TODO: remember to start using the db

# TODO: STOP JUST USING THE ID TO ACCESS POKEMON DIRECTLY!!!!!! use the numbers to pick a random species, then add EVERY SINGLE VARIETY
# TODO: TO THE LIST OF POKEMON!!! For example:
# randomly chosen SPECIES: lycanroc, spearow, fearow, charizard, pikachu
# randomly chosen POKEMON: lycanroc-midday, lycanroc-dusk, lycanroc-midnight, spearow, fearow, charizard, charizard mega x, charizard mega y, gmax charizard, pikachu, pikachu costumes, pikachu caps (???), gmax pikachu


class SmashOrPassView(discord.ui.View):
    choice: Optional[bool]

    def __init__(self, player_id: int):
        super().__init__()
        self.player_id = player_id
        self.choice = None

    @discord.ui.button(label='Smash', style=discord.ButtonStyle.green)
    async def smash(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None)
        self.choice = True
        self.stop()

    @discord.ui.button(label='Pass', style=discord.ButtonStyle.red)
    async def pass_is_a_reserved_keyword_lmao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None)
        self.choice = False
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def stop_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None)
        self.choice = None  # trigger the same behaviour as a game timeout
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("That isn't your game! To start a game, use the `pokesmash` command.",
                                                    ephemeral=True)
        return interaction.user.id == self.player_id

# await interaction.response.send_message("That isn't your game! To start a game, use the `pokesmash` command.",
#                                                    ephemeral=True)


@dataclass
class SmashGameState:
    message: discord.Message  # the message for this player's game
    # dict of smashes/passes. e.g. {3: True, 9: False}
    decisions: dict[int, bool] = field(default_factory=dict)


class SmashOrPass(commands.Cog):

    bot: commands.Bot
    active_games: dict[int, SmashGameState]  # user ID: thier game state

    def __init__(self, bot, db_url) -> None:
        self.bot = bot
        self.active_games = {}
        self.api = PokeWrapper(db_url)

    # @profile
    def make_embed(self, pokemon: dict, first: bool) -> discord.Embed:
        '''
        argument `pokemon` is one of the dicts returned from PokeWrapper.species_details.
        '''
        fixed_desc = pokemon['pokedex'].replace(u"\f", u"\n") \
            .replace(u'\u00ad\n', u'') \
            .replace(u'\u00ad', u'') \
            .replace(u' -\n', u' - ') \
            .replace(u'-\n', u'-') \
            .replace(u'\n', u' ')
        return discord.Embed.from_dict({
            "type": "rich",
            "title": "Smash or Pass?" if first else "How about this one?",
            # changes the title for follow-ups
            "description": f"#{pokemon['id']} - {pokemon['name']}",
            "color": 0xFF0000,
            "image": {
                "url": pokemon['sprite'],
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
    async def play_game(self, ctx: commands.Context, *args: str) -> None:
        player_id = ctx.message.author.id
        if player_id in self.active_games.keys():
            await ctx.send("You already have a game going!",
                           reference=self.active_games[player_id].message)
            return
        game_msg: discord.Message = await ctx.send(f"{ctx.message.author}'s Game")
        self.active_games[player_id] = SmashGameState(game_msg, {})
        for species in ["pikachu"]:
            if not await self.update_game(player_id, species):
                break
        # TODO: store the results
        temp_results_for_testing = self.active_games[player_id].decisions
        self.active_games.pop(player_id)
        await game_msg.edit(content=f"results:{temp_results_for_testing}", embed=None, view=None)

    @commands.command(name="pokesmashstop")
    async def stop_game(self, ctx: commands.Context, *args: str) -> None:
        if ctx.message.author.id not in self.active_games.keys():
            await ctx.send("You don't have a game running!")
            return
        self.active_games.pop(ctx.message.author.id)
        await ctx.send("Stopped your game.")

    async def update_game(self, player_id: int, species_identifier: Union[int, str]) -> bool:
        ''' Does a single iteration of the game. Takes a species identifier (id or name) and does every pokemon in that species.
        e.g. for species == 706 or species == "goodra", do pokemon goodra and goodra-hisui.
        The IDs used to save the response should be POKEMON IDs, NOT SPECIES IDs!!! So that the response for each form can be stored.

        returns True if turn was successful, False if game was cancelled or timed out.
        '''
        all_pokemon = self.api.species_details(species_identifier)
        game_msg = self.active_games[player_id].message
        if all_pokemon == []:
            await game_msg.edit(content="The API isn't working right now!")
            return False
        else:
            first = True
            for pokemon in all_pokemon:
                smash_view = SmashOrPassView(player_id)
                await game_msg.edit(embed=self.make_embed(pokemon, first), view=smash_view)
                first = False
                await smash_view.wait()
                if smash_view.choice is None:  # timeout or cancelled game
                    return False
                else:
                    self.active_games[player_id].decisions[pokemon['id']] = smash_view.choice
            return True  # only return a success when all pokemon are 


# extension setup function
async def setup(bot: commands.Bot) -> None:
    load_dotenv()
    db_url = getenv("DATABASE_URL")
    await bot.add_cog(SmashOrPass(bot, db_url))
