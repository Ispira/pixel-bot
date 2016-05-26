#Botmaster commands v1.0.0
import discord
from discord.ext import commands

from bot_globals import display_purges, server_list
from checks import *

forbidden = "I don't have permission to do that."

class Botmaster():
    def __init__(self, bot):
        self.bot = bot
    
    ## Completely exit the bot
    @commands.command()
    @allowed(1, '$')
    async def quit(self):
        await self.bot.say("Bye...")
        await self.bot.logout()
    
    ## Purge messages
    @commands.command(pass_context=True)
    @allowed(1, '$')
    async def purge(self, ctx, pamt: int, ptype: str, *, parg: str = ""):
        pamt += 1
        try:
            #All messages
            if ptype == "all":
                def check(m):
                    return True
                purged = "everyone"
            #Messages from a specific user
            elif ptype == "user":
                def check(m):
                    return m.author in ctx.message.mentions
                purged = ctx.message.mentions[0].mention
            #Messages from a specific role
            elif ptype == "role":
                def check(m):
                    if ctx.message.role_mentions[0] in m.author.roles:
                        return True
                purged = ctx.message.role_mentions[0].mention
            #Incorrect usage
            else:
                await self.bot.say("Usage: `$purge <amount> <all | user @User | role @Role>`")
                return
            
            #Purge it!
            counter = await self.bot.purge_from(ctx.message.channel, limit=pamt, check=check)
            #Send a notice if the config says so
            if display_purges:
                await self.bot.say("{0.mention} purged {1} message(s) from {2}."
                .format(ctx.message.author, len(counter), purged))
        except discord.Forbidden:
            await self.bot.say(forbidden)
    
    ## Change a user's nickname
    @commands.command()
    @allowed(1, '$')
    async def nick(self, user: discord.Member, *, nick: str):
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
    
    ## Change the bot's status
    @commands.command()
    @allowed(1, '$')
    async def playing(self, *, playing: str):
        if playing.lower() == "!none":
            status = None
        else:
            status = discord.Game(name=playing)
        await self.bot.change_status(game=status)
        await self.bot.say("I'm playing {0}".format(playing))
    
    ## Get an invite to a server the bot is connected to, if possible.
    @commands.command(pass_context=True)
    @allowed(1, '$')
    async def inviteme(self, ctx, *, name: str):
        for serv in server_list:
            if serv.name == name:
                try:
                    invite = await self.bot.create_invite(serv.default_channel)
                    await self.bot.send_message(ctx.message.author,
                    "Invite to {0}: {1}".format(name, invite))
                except HTTPException as error:
                    await self.bot.say("Error getting invite: {0}"
                    .format(error))
        
def setup(bot):
    bot.add_cog(Botmaster(bot))
