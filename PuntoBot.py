import random
import asyncio
import aiohttp
import rule34
import discord
from os import getenv
from dotenv import load_dotenv
from requests import get
from json import loads
from html import escape
from discord import Game
from discord.ext.commands import Bot

PREFIX = "##"
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
#Get at discordapp.com/developers/applications/me
client = Bot(command_prefix=PREFIX)
client.remove_command("help")

###RULE34 GRABBER
rule34 = rule34.Rule34(asyncio.get_event_loop())

previous = None

@client.command(name = '8ball',
                description = "Answers from the great beyond. (Answers a yes/no question.)",
                aliases = ['eight_ball', 'eightball', '8-ball'])
async def eight_ball(ctx):
    with open("8ball.txt", "r") as file:
        responses = file.readlines()
    await ctx.send(f"{random.choice(responses)}, {ctx.message.author.mention}")

@client.command(name = "power",
                description = "Totally exponential! Used: power [number] [power]")
async def power(ctx, number, power):
    try:
        pow_value = float(number) ** float(power)
        await ctx.send(f"{number} to the power of {power} is {pow_value}.")
    except:
        await ctx.send("Not a number!")

@client.command(name = "r34",
                description = "used by war criminals to locate cheese pizza. Used: r34 [keyword]")
async def r34(ctx, *args):
    keyword = ' '.join(args)
    print("getting r34\nkeyword = " + keyword)
    results = await rule34.getImages(keyword)
    if results is None:
        await ctx.send("No results.")
    else:
        choice = random.choice(results)
        message = await ctx.send(choice.file_url)
        await message.add_reaction("\U0001F6AB")
        try:
            await client.wait_for("message",
                                  check = lambda r : r.content in ("tags", "tags?", "tag", "tag?"))
            message = await ctx.send(f"tags: `{', '.join(choice.tags)}`")
            await message.add_reaction("\U0001F6AB")
        except asyncio.TimeoutError:
            print("nobody wanted tags for " + choice.file_url)
       
@client.command(name = "e621",
                description = "used by me to locate cheese graters. Used: e621 [keyword(s)]")
async def e621(ctx, *args):
    url = "https://www.e621.net/posts.json?limit=100&tags="
    keyword = '+'.join([escape(arg) for arg in args])
    url += keyword
    print("getting e621\nkeyword = " + keyword)
    headers = {'User-Agent': 'cute152DiscordBot'}
    resp = get(url, headers = headers)
    parsed = loads(resp.text)
    if parsed['posts']: #if list not empty
        choice = random.choice(parsed['posts'])
        message = await ctx.send(choice['file']['url'])
        await message.add_reaction("\U0001F6AB") # add the delete reaction
    else:
        await ctx.send("No results.")

@client.command(name = "e926",
                description = "how nice. Used: e926 [keyword(s)]")
async def e926(ctx, *args):
    await e621(ctx, "rating:safe", *args)

@client.command(name = "help",
                description = "displays a list of all commands.")
async def help(ctx):
    helpMessage = discord.Embed(title = "Help", color=0xFF8000)
    helpMessage.set_author(name="Jeffrey Epstein", url="https://google621.neocities.org")
    helpMessage.set_thumbnail(url="https://pbs.twimg.com/profile_images/1315716250706882563/Z1eDpiVY_400x400.jpg")
    for command in client.commands:
        helpMessage.add_field(name = PREFIX + command.name,
                              value = command.description if command.description else "[no description added]",
                              inline = False)
    await ctx.send(embed = helpMessage)

@client.command(name = "pyramid",
                description = "create a sick awesome legit pyramid of teh ultamte dooom!!!!!!1!11 Used: pyramid [levels]")
async def pyramid(ctx, levels_str):
    try: levels = int(levels_str)
    except: await ctx.send("that isnt a number")
    pyramid = "```"
    width = (levels * 2) - 1
    for x in range(1, levels + 1):
        pyramid += " " * (levels - x)
        pyramid += "* " * x
        pyramid += " " * (levels - (x + 1))
        pyramid += "\n"
    pyramid += "```"
    await ctx.send(pyramid)

@client.event
async def on_reaction_add(reaction, user):
    if not user.bot and reaction.emoji == "\U0001F6AB":
        await reaction.message.delete()

#SET BOT STATE
@client.event
async def on_ready():
    print("Trying to set presence... ")
    await client.change_presence(activity=Game(name="gaming, like a boss"))
    print("Logged in as " + client.user.name)

#@client.event
#async def on_command_error(ctx, error):
#    await ctx.send("you typed it wrong, brainlet!")

client.run(TOKEN)
