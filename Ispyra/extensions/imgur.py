#Imgur extension v1.0.0
import random
import asyncio

from discord.ext import commands
from imgurpython import ImgurClient
from checks import *

imgur_config = open("./extensions/imgur/config.txt").read().splitlines()

imgur = ImgurClient(imgur_config[0], imgur_config[1])

class Imgur():
    def __init__(self, bot):
        self.bot = bot      
    
    @commands.command()
    @allowed(0, '|')
    async def imgur(self, arg: str, *, query: str = ""):
        if arg.lower() == "reddit":
            result = self.bot.loop.run_in_executor(None,
            imgur.subreddit_gallery, query)
        elif arg.lower() == "search":
            result = self.bot.loop.run_in_executor(None,
            imgur.gallery_search, query)
        elif arg.lower() == "random":
            result = self.bot.loop.run_in_executor(None,
            imgur.gallery_random)
        elif arg.lower() == "top" or arg.lower() == "hot":
            sort = "viral"
            if query.lower() == "new":
                sort = query
            result = self.bot.loop.run_in_executor(None,
            imgur.gallery, arg.lower(), sort)
        else:
            await self.bot.say(
                "Usage: `|imgur <reddit <subreddit> | search <query> | random | top [new] | hot [new]>`")
            return
        
        while True:
            await asyncio.sleep(0.25)
            if result.done():
                break
        choice = random.choice(result.result())
        await self.bot.say(choice.link)
    
def setup(bot):
    bot.add_cog(Imgur(bot))