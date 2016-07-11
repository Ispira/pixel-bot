import asyncio
import xkcd
#uncomment the following line to gain the ability to fly
#import antigravity

from discord.ext import commands as c

class XKCD:
    """A plugin for those on the internet with good humor."""
    def __init__(self, bot):
        self.bot = bot

    # Helper function for getting comics
    async def get_comic(self, comic, number = None):
        case = {
            "latest": lambda: xkcd.getLatestComic(),
            "random": lambda: xkcd.getRandomComic(),
            "number": lambda: xkcd.getComic(number),
        }
        function = case.get(comic, None)
        comic = self.bot.loop.run_in_executor(None, function)
        while True:
            await asyncio.sleep(0.25)
            if comic.done():
                comic = comic.result()
                break
        try:
            link = comic.getImageLink()
            title = comic.getAsciiTitle().decode("ascii")
            alt_text = comic.getAsciiAltText().decode("ascii")
            number = comic.number
            return f"{number} - {link}\n**Title:** {title}\n**Alt:** {alt_text}"
        except AttributeError:
            return "\U00002754 Can't find that comic."

    @c.group(pass_context=True)
    async def xkcd(self, ctx):
        """Get comics from xkcd!
        
        Running the command without arguments will display the latest comic.
        """
        if ctx.invoked_subcommand is None:
            comic = await self.get_comic("latest")
            await self.bot.say(comic)
    
    @xkcd.command(name="random")
    async def xkcd_random(self):
        """Get a random xkcd comic."""
        comic = await self.get_comic("random")
        await self.bot.say(comic)
    
    @xkcd.command(name="number")
    async def xkcd_number(self, number: int):
        """Get an xkcd comic by number."""
        comic = await self.get_comic("number", number)
        await self.bot.say(comic)
    
    @c.group(name="import")
    async def xkcd_import(self, module):
        """Related, since this bot is programmed in Python."""
        if module == "antigravity":
            comic = await self.get_comic("number", 353)
            await self.bot.say(comic)

def setup(bot):
    bot.add_cog(XKCD(bot))
