#User commands v1.1.0
import xkcd
import asyncio
from discord.ext import commands
from bot_globals import version, bot_masters, server_list
from checks import prefix

class User():
    def __init__(self, bot):
        self.bot = bot
    
    ## Apparently ping commands are hip
    @commands.command()
    @prefix('|')
    async def ping(self):
        """Pong."""
        await self.bot.say("Pong.")
    
    ## Version information
    @commands.command()
    @prefix('|')
    async def info(self):
        """Display information about this bot."""
        await self.bot.say("Ispyra {0} by Ispira (https://github.com/Ispira/Ispyra)"
        .format(version))
    
    ## Bot status
    @commands.command()
    @prefix('|')
    async def status(self):
        """Display number of botmasters, and connected servers."""
        await self.bot.say("Servers: {0} | Botmasters: {1}"
        .format(len(server_list), len(bot_masters)))
    
    ## List names of currently connected servers
    @commands.command()
    @prefix('|')
    async def servers(self):
        """List the names of all currently connected servers."""
        server_names = []
        for serv in server_list:
            server_names.append(serv.name)
        await self.bot.say(" | ".join(server_names))
    
    ## XKCD!
    @commands.command()
    @prefix('|')
    async def xkcd(self, number: int = None):
        """Get a comics from XKCD. Use -1 for random comic."""
        if number is None:
            comic = self.bot.loop.run_in_executor(
                None, xkcd.getLatestComic)
        elif number is -1:
            comic = self.bot.loop.run_in_executor(
                None, xkcd.getRandomComic)
        else:
            comic = self.bot.loop.run_in_executor(
                None, xkcd.getComic, number)
        while True:
            await asyncio.sleep(0.25)
            if comic.done():
                comic = comic.result()
                break
        try:
            link = comic.getImageLink()
            title = comic.getTitle()
        except AttributeError:
            await self.bot.say("Comic {0} not found.".format(number))
        await self.bot.say("{0}\n{1}".format(title, link))

def setup(bot):
    bot.add_cog(User(bot))
