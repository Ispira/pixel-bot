#User commands v1.1.0
import xkcd
import asyncio
import discord
from discord.ext import commands
from bot_globals import version, bot_masters, server_list, extensions_loaded
from checks import allowed, permission

class User():
    def __init__(self, bot):
        self.bot = bot
    
    ## Apparently ping commands are hip
    @commands.command()
    @allowed()
    async def ping(self):
        """Pong."""
        await self.bot.say("Pong.")
    
    ## Version information
    @commands.command()
    @allowed()
    async def info(self):
        """Display information about this bot."""
        await self.bot.say("Ispyra {0} by Ispira (https://github.com/Ispira/Ispyra)"
        .format(version))
    
    ## Bot status
    @commands.command()
    @allowed()
    async def status(self):
        """Display bot status."""
        await self.bot.say("Servers: {0} | Botmasters: {1} | Extensions: {2}"
        .format(len(server_list), len(bot_masters), len(extensions_loaded)))
    
    ## Loaded extensions
    @commands.command()
    @allowed()
    async def extensions(self):
        """List of loaded extensions."""
        await self.bot.say(" | ".join(extensions_loaded))
    
    ## XKCD!
    @commands.command()
    @allowed()
    async def xkcd(self, number: int = None):
        """Get a comics from XKCD. Use -1 for a random comic."""
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
    
    ## Change a user's nickname
    @commands.command(no_pm=True)
    @allowed()
    @permission(manage_nicknames=True)
    async def nick(self, user: discord.Member, *, nick: str):
        """Change a user's nickname."""
        try:
            #Remove nickname if the nick is set to '!none'
            if nick.lower() == "!none":
                await self.bot.change_nickname(user, None)
            else:
                await self.bot.change_nickname(user, nick)
            await self.bot.say("Nickname set.")
        except discord.Forbidden:
            await self.bot.say(forbidden)
        except discord.HTTPException as error:
            await bot.say("Unable to change nickname: {0}"
            .format(error))

def setup(bot):
    bot.add_cog(User(bot))
