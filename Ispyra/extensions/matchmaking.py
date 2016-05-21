#Matchmaking commands
from discord.ext import commands

from bot_globals import db
from checks import *

class Matchmaking():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @prefix('^')
    @allowed(0)
    async def matchmaking(self):
        await self.bot.say("Coming soon.")

def setup(bot):
    bot.add_cog(Matchmaking(bot))
