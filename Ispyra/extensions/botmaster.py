#Botmaster commands
from discord.ext import commands

from checks import *

class Botmaster():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @allowed(1, '$')
    async def quit(self):
        await self.bot.say("Bye...")
        await self.bot.logout()
        
def setup(bot):
    bot.add_cog(Botmaster(bot))
