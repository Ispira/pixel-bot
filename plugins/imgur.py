import asyncio
import json
import random

from discord.ext import commands as c
from imgurpython import ImgurClient

with open("plugins/settings/imgur.json") as imgr:
    config = json.load(imgr)

class Imgur:
    """The most awesome images on the internet!
    
    This plugin allows basic searching on Imgur including subreddits.
    
    Warning: Searching on subreddits cannot be easily moderated, therefore it is
    extremely easy for a user to post images from an nsfw subreddit to whatever
    channel the bot is enabled in if this plugin is enabled without modification.
    The subreddit command can be disabled by changing 'enabled=True' to 'enabled=False'
    in the plugin's main file: 'plugins/imgur.py' on line 53.
    """
    def __init__(self, bot):
        self.bot = bot
        self.client = ImgurClient(config["client_id"], config["client_secret"])
    
    @c.group(pass_context=True)
    async def imgur(self, ctx):
        """Search on Imgur!"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Zoinks! You've taken a wrong turn! Try `help imgur`.")
    
    # Helper function to actually get/post the images
    async def post_image(self, request, query=None):
        case = {
            "subreddit": lambda: self.client.subreddit_gallery(query),
            "search"   : lambda: self.client.gallery_search(query),
            "random"   : lambda: self.client.gallery_random(),
            "top"      : lambda: self.client.gallery("top"),
            "hot"      : lambda: self.client.gallery("hot"),
            "rehost"   : lambda: self.client.upload_from_url(query),
        }
        function = case.get(request, None)
        image = self.bot.loop.run_in_executor(None, function)
        while True:
            await asyncio.sleep(0.25)
            if image.done():
                image = image.result()
                break
        if request == "rehost":
            await self.bot.say(image.get("link", None))
        else:
            await self.bot.say(random.choice(image).link)

    @imgur.command(name="sub", aliases=["subreddit", "reddit", "r/"], enabled=True)
    async def imgur_subreddit(self, subreddit: str):
        """Get an image from a subreddit."""
        await self.post_image("subreddit", subreddit)

    @imgur.command(name="search")
    async def imgur_search(self, *, query: str):
        """Search Imgur for (almost) anything."""
        await self.post_image("search", query)
    
    @imgur.command(name="random")
    async def imgur_random(self):
        """One free random image."""
        await self.post_image("random")
    
    @imgur.command(name="viral")
    async def imgur_viral(self, section: str = "top"):
        """Get one of the most viral images of the day.
        
        Section may be either 'top' or 'hot' and will get an image based on that criteria."""
        section = section.lower()
        if section != "top":
            section = "hot"
        await self.post_image(section)
    
    @imgur.command(name="rehost")
    async def imgur_rehost(self, url: str):
        """Rehost an image from any link to Imgur."""
        await self.post_image("rehost", url)

def setup(bot):
    bot.add_cog(Imgur(bot))
