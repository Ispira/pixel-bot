#Imgur extension v1.1.0
import random
import asyncio
from discord.ext import commands
from imgurpython import ImgurClient
from checks import prefix

imgur_config = open("./extensions/imgur/config.txt").read().splitlines()

imgur = ImgurClient(imgur_config[0], imgur_config[1])

class Imgur():
    def __init__(self, bot):
        self.bot = bot
    
    ## Imgur search
    @commands.group(pass_context=True)
    @prefix('|')
    async def imgur(self, ctx):
        """Search on Imgur!"""
        #Straight from the 404
        if ctx.invoked_subcommand is None:
            await self.bot.say("Zoinks! You've taken a wrong turn. `|help Imgur`")
    
    async def post_image(self, itype, query=None):
        case = {
            "reddit": lambda: imgur.subreddit_gallery(query),
            "search": lambda: imgur.gallery_search(query),
            "random": lambda: imgur.gallery_random(),
            "top"   : lambda: imgur.gallery("top"),
            "hot"   : lambda: imgur.gallery("hot"),
        }
        function = case.get(itype, None)
        image = self.bot.loop.run_in_executor(None, function)
        while True:
            await asyncio.sleep(0.25)
            if image.done():
                image = image.result()
                break
        await self.bot.say(random.choice(image).link)

    #Subreddits
    @imgur.command()
    async def reddit(self, sub: str):
        """Get an image from the specified subreddit."""
        await self.post_image("reddit", sub)
    
    #Search
    @imgur.command()
    async def search(self, query: str):
        """Search imgur for almost anything."""
        await self.post_image("search", query)
    
    #Random lol xD :3
    @imgur.command()
    async def random(self):
        """One free random image."""
        await self.post_image("random")
    
    #Like a virus!
    @imgur.command()
    async def viral(self, section: str = "top"):
        """Get one of the most viral images of the day.
        
        Section may be either 'top' or 'hot'."""
        section = section.lower()
        if section != "top": section = "hot"
        await self.post_image(section)
    
def setup(bot):
    bot.add_cog(Imgur(bot))