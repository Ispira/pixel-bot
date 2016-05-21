#User commands
from discord.ext import commands

from bot_globals import version, bot_masters, server_list
from checks import *

class User():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @allowed(0, '|')
    async def info(self):
        await self.bot.say("Ispyra {0} by Ispira (https://github.com/Ispira/Ispyra)"
        .format(version))

def setup(bot):
    bot.add_cog(User(bot))
