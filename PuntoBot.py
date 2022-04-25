import asyncio
from datetime import datetime
import random
import html
from os import getenv
import yiffgen

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import requests
from rule34 import Rule34

PREFIX = "=="
DELETE_EMOJI = "\U0001F6AB"
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
# Get at discordapp.com/developers/applications/me
client = Bot(command_prefix=PREFIX)
client.remove_command("help")

# RULE34 GRABBER
rule34 = Rule34(asyncio.get_event_loop())


@client.command(name='8ball',
                description="Answers from the great beyond. (Answers a yes/no question.)",
                aliases=['eight_ball', 'eightball', '8-ball'])
async def eight_ball(ctx):
    with open("8ball.txt", "r") as file:
        responses = file.readlines()
    await ctx.send(f"{random.choice(responses).strip()}, {ctx.message.author.mention}")


@client.command(name="exp",
                description="Totally exponential! Used: exp [number] [power]")
async def exp(ctx, number, power):
    try:
        pow_value = float(number) ** float(power)
        await ctx.send(f"{number} to the power of {power} is {pow_value}.")
    except ValueError:
        await ctx.send("Not a number!")

client.make_search_result_embed = lambda title_name, tags, artists, image_url, logo_url, post_url : discord.Embed.from_dict({
          "type": "rich",
          "title": f"{title_name} Link",
          "description": "**You searched for:** " + ' '.join([html.escape(tag) for tag in tags]),
          "color": 0xfdb328,
          "fields": [
            {
              "name": "Artist(s)",
              "value": ' '.join(artists)
            }
          ],
          "image": {
            "url": image_url,
            "height": 0,
            "width": 0
          },
          "thumbnail": {
            "url": logo_url,
            "height": 0,
            "width": 0
          },
          "author": {
            "name": "Punto to the rescue:"
          },
          "url": post_url
        })

@client.command(name="r34",
                description="Used by war criminals to procure cheese pizza. Used: r34 [keyword]")
async def r34(ctx, *args):
    keyword = ' '.join(args)
    #print("getting r34\nkeyword = " + keyword)
    results = await rule34.getImages(keyword)
    if results is None:
        await ctx.send("No results.")
    else:
        choice = random.choice(results)
        r34_embed = client.make_search_result_embed("r34", 
            args, 
            ["r34 doesn't give artists lol"], 
            choice.file_url, 
            f"https://static.wikia.nocookie.net/joke-battles/images/2/24/Rule34_logo.png", 
            f"https://rule34.xxx/index.php?page=post&s=view&id={choice.id}")
        message = await ctx.send(embed=r34_embed)
        log_user_request(ctx.author, message)
        await message.add_reaction(DELETE_EMOJI)


client.previous_choice = {'id': -1}
@client.command(name="e621",
                description="Used by furbys to procure cheese graters. Used: e621 [keyword(s)]")
async def e621(ctx, *args):
    url = "https://www.e621.net/posts.json?limit=100&tags="
    keyword = '+'.join([html.escape(arg) for arg in args])
    url += keyword
    print(f"getting e621 for '{ctx.message.author}' \nkeyword = {keyword}")
    headers = {'User-Agent': 'cute152DiscordBot'}
    resp = requests.get(url, headers=headers)
    parsed = resp.json()
    posts = [x for x in parsed['posts'] if x['id'] != client.previous_choice['id']]
    if posts:  # if list not empty
        choice = random.choice(posts)
        image_url = choice['file']['url']
        #if choice['rating'] != 's': 
        #    image_url = f"|| {image_url} ||"
        e6_embed = client.make_search_result_embed("e621", args, choice["tags"]["artist"], image_url, "https://en.wikifur.com/w/images/d/dd/E621Logo.png", f"http://www.e621.net/posts/{choice['id']}")
        message = await ctx.send(embed=e6_embed)
        client.previous_choice = choice
        log_user_request(ctx.author, message)
        await message.add_reaction(DELETE_EMOJI)  # add the delete reaction
    else:
        await ctx.send("No results.")

@client.command(name="comments",
                description="find the top and bottom comments of the previous esix post. has no arguments.")
async def comments(ctx):
    if client.previous_choice['id'] == -1:
        await ctx.send("The bot hasn't sent an image yet!")
    else:
        url = 'https://e621.net/comments.json?commit=Search&group_by=comment&search%5Border%5D=id_desc&search%5Bpost_tags_match%5D=id%3A'
        url += str(client.previous_choice['id'])
        headers = {'User-Agent': 'cute152DiscordBot'}
        resp = requests.get(url, headers=headers)
        parsed = resp.json()
        if "comments" in parsed:
            await ctx.send("Post has no comments.")
        else:
            parsed = sorted(parsed, key=lambda x:x['score'])
            lowest_comment = parsed[0]
            highest_comment = parsed[-1]
            await ctx.send(f"Lowest rated comment with score {lowest_comment['score']}\n`{lowest_comment['body']}`")
            await ctx.send(f"Highest rated comment with score {highest_comment['score']}\n`{highest_comment['body']}`")
    
@client.command(name="zorn",
                description="for when you cant decide what kind of zorn youre going to zerk off to")
async def zorn_generator(ctx):
    await ctx.send(yiffgen.make_zorn())

@client.command(name="ship",
                description="hottest new ship on the internet")
async def ship_generator(ctx):
    pairing = yiffgen.make_pairing(1, 3)
    if yiffgen.pogg_ing:
        pairing += "\nOMG best ship!!!! i FUCKING LOVE typhlosion x feraligatr its so awesome typhlosion is such an EPIC POWER BOTTOM!!!"
    await ctx.send(pairing)
    if yiffgen.pogg_ing:
        await e621(ctx, "typhlosion", "feraligatr", "order:score", "rating:explicit")
        yiffgen.pogg_ing = False

@client.command(name="forcepog",
                description="aaaaaaaaa",
                hidden=True)
async def forcepog(ctx):
    yiffgen.pogg_ing = True

requests_log = []
def log_user_request(request_user, sent_message):
    requests_log.append((request_user.id, sent_message.id))

@client.command(name="e926",
                description="No adults allowed in the treehouse club. Used: e926 [keyword(s)]")
async def e926(ctx, *args):
    await e621(ctx, "rating:safe", *args)


@client.command(name="help",
                description="Displays this list of commands.")
async def help(ctx):
    help_message = discord.Embed(title="Help", color=0xFF8000)
    help_message.set_author(name="Jeffrey Epstein", url="https://google621.neocities.org")
    help_message.set_thumbnail(url="https://pbs.twimg.com/profile_images/1315716250706882563/Z1eDpiVY_400x400.jpg")
    for command in client.commands:
        if not command.hidden:
            help_message.add_field(name=PREFIX + command.name,
                                   value=command.description if command.description else "[no description added]",
                                   inline=False)
    await ctx.send(embed=help_message)


@client.command(name="pyramid",
                description="create a sick awesome epic pyramid of teh ultamte dooom!!!!!!1!11 Used: pyramid [levels]")
async def pyramid(ctx, levels_str):
    try:
        levels = int(levels_str)
        result = "```"
        for x in range(1, levels + 1):
            result += " " * (levels - x)
            result += "* " * x
            result += " " * (levels - (x + 1))
            result += "\n"
        result += "```"
        await ctx.send(result)
    except ValueError:
        await ctx.send("That isn't a number.")


@client.command(name="imitate",
                description="Can you say that again?")
async def imitate(ctx):
    retard = ctx.message.content[len('##imitate '):]
    await ctx.send(retard)


@client.command(name="give_log",
                description="Get deleted message logs",
                hidden=True)
async def give_log(ctx):
    if ctx.author.id == 303228582740885514:
        await ctx.send(file=discord.File("deleted.log"))


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot and reaction.emoji == DELETE_EMOJI:
        if (user.id, reaction.message.id) in requests_log:
            requests_log.remove((user.id, reaction.message.id))
            await reaction.message.delete()


@client.event
async def on_message_delete(message: discord.Message):
    if message.author.id == 303228582740885514:  # ignore my messages :)
        return
    with open("deleted.log", "a") as f:
        f.write(f"{message.author.display_name}: '{message.content}'\n")
        f.write(f"Deleted at {datetime.now()}\n\n")
    ctx = await client.get_context(message)
    time_since = datetime.utcnow() - message.created_at
    if message.content.startswith('##e621 ') and time_since.total_seconds() < 30:
        await ctx.send(f'why so quick to delete your message, {message.author.mention}?')


# SET BOT STATE
@client.event
async def on_ready():
    print("Trying to set presence... ")
    await client.change_presence(activity=discord.Game(name="gaming, like a boss"))
    print("Logged in as " + client.user.name)


client.run(TOKEN)
