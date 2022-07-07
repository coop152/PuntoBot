import asyncio
import html
import random
from json import JSONDecodeError
from typing import List, Tuple, Union

import discord.ext.commands as commands
import requests
from discord import Embed, Member, Message, User, Reaction
from rule34 import Rule34


class ImageGetters(commands.Cog):
    # static members
    DELETE_EMOJI = "\U0001F6AB"  # 🚫
    REQUEST_HEADERS = {'User-Agent': 'cute152DiscordBot'}
    rule34 = Rule34(asyncio.get_event_loop())

    # instance members
    bot: commands.Bot
    previous_id: int
    requests_log: List[Tuple[int, int]]

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.previous_id = -1
        self.requests_log = []

    @commands.command(name="r34",
                      description="Used by war criminals to procure cheese pizza. Used: r34 [keyword]")
    async def r34(self, ctx: commands.Context, *args: str) -> None:
        keyword = ' '.join(args)
        print(
            f"getting rule34 for '{ctx.message.author}' \nkeyword = {keyword}")
        results = await self.rule34.getImages(keyword)
        if results is None:
            await ctx.send("No results.")
        else:
            choice = random.choice(results)
            r34_embed = self.make_result_embed("r34",
                                               args,
                                               ["r34 doesn't give artists lol"],
                                               choice.file_url,
                                               "https://static.wikia.nocookie.net/joke-battles/images/2/24/Rule34_logo.png",
                                               f"https://rule34.xxx/index.php?page=post&s=view&id={choice.id}")
            message = await ctx.send(embed=r34_embed)
            self.log_user_request(ctx.message.author, message)
            await message.add_reaction(self.DELETE_EMOJI)

    @commands.command(name="e621",
                      description="Used by furbys to procure cheese graters. Used: e621 [keyword(s)]")
    async def e621(self, ctx: commands.Context, *args: str) -> None:
        url = "https://www.e621.net/posts.json?limit=100&tags="
        keyword = '+'.join([html.escape(arg) for arg in args])
        url += keyword
        print(f"getting e621 for '{ctx.message.author}' \nkeyword = {keyword}")
        resp = requests.get(url, headers=self.REQUEST_HEADERS)
        try:
            parsed = resp.json()
        except JSONDecodeError:
            print("Error while decoding json response. Response:\n")
            print(resp)
            await ctx.send("The API is broken! Send an improvised explosive device to Kyle's house to alert him of this extremely important issue.")
            return
        posts = [x for x in parsed['posts'] if x['id']
                 != self.previous_id]
        if posts:  # if list not empty
            choice = random.choice(posts)
            image_url = choice['file']['url']
            e6_embed = self.make_result_embed(
                "e621", args, choice["tags"]["artist"], image_url, "https://en.wikifur.com/w/images/d/dd/E621Logo.png", f"http://www.e621.net/posts/{choice['id']}")
            message = await ctx.send(embed=e6_embed)
            self.previous_id = choice["id"]
            self.log_user_request(ctx.message.author, message)
            # add the delete reaction
            await message.add_reaction(self.DELETE_EMOJI)
        else:
            await ctx.send("No results.")

    @commands.command(name="e926",
                      description="No adults allowed in the treehouse club. Used: e926 [keyword(s)]")
    async def e926(self, ctx: commands.Context, *args: str) -> None:
        await self.e621(ctx, "rating:safe", *args)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: User) -> None:
        if not user.bot and reaction.emoji == self.DELETE_EMOJI:
            if (user.id, reaction.message.id) in self.requests_log:
                self.requests_log.remove((user.id, reaction.message.id))
                await reaction.message.delete()

    def make_result_embed(self, title_name: str, tags: Tuple[str], artists: List[str],
                          image_url: str, logo_url: str, post_url: str) -> Embed:
        embed_as_dict = {
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
        }
        return Embed.from_dict(embed_as_dict)

    def log_user_request(self, request_user: Union[User, Member], sent_message: Message) -> None:
        self.requests_log.append((request_user.id, sent_message.id))

    @commands.command(name="e621count",
                      description="Get the number of posts for an e621 tag/tags.")
    async def e6_count(self, ctx: commands.Context, *args: str) -> None:
        url = "https://e621.net/tags.json?search[name_matches]="
        if (len(args) != 1):
            await ctx.send("Give a single tag.")
            return
        url += html.escape(args[0])
        print(
            f"getting e621 tag count for '{ctx.message.author}' \ntag = {args[0]}")
        resp = requests.get(url, headers=self.REQUEST_HEADERS)
        parsed = resp.json()
        if parsed == {"tags": []}:  # magic result for an invalid tag
            await ctx.send("Couldn't find that tag.")
            return
        else:
            await ctx.send(f"The tag '{args[0]}' has {parsed[0]['post_count']} posts.")

    @commands.command(name="comments",
                      description="find the top and bottom comments of the previous e621 post. has no arguments.")
    async def comments(self, ctx: commands.Context) -> None:
        if self.previous_id == -1:
            await ctx.send("The bot hasn't sent an image yet!")
        else:
            url = 'https://e621.net/comments.json?commit=Search&group_by=comment&search%5Border%5D=id_desc&search%5Bpost_tags_match%5D=id%3A'
            url += str(self.previous_id)
            resp = requests.get(url, headers=self.REQUEST_HEADERS)
            parsed = resp.json()
            if "comments" in parsed:
                await ctx.send("Post has no comments.")
            else:
                parsed = sorted(parsed, key=lambda x: x['score'])
                lowest_comment = parsed[0]
                highest_comment = parsed[-1]
                await ctx.send(f"Lowest rated comment with score {lowest_comment['score']}\n`{lowest_comment['body']}`")
                await ctx.send(f"Highest rated comment with score {highest_comment['score']}\n`{highest_comment['body']}`")


# extension setup function
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ImageGetters(bot))
