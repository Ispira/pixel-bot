#Botmaster commands v1.0.2
import discord
from discord.ext import commands

from bot_globals import display_purges, server_list
from checks import *

forbidden = "I don't have permission to do that."

class Botmaster():
    def __init__(self, bot):
        self.bot = bot
    
    ## Purge messages
    @commands.command(pass_context=True)
    @prefix('$')
    @permission(manage_messages=True)
    async def purge(self, ctx, pamt: int, ptype: str, *, parg: str = ""):
        """Purge messages."""
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
    @prefix('$')
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
    
    ## Change the bot's status
    @commands.command()
    @prefix('$')
    @botmaster()
    async def playing(self, *, playing: str):
        """Change the bot's playing status."""
        if playing.lower() == "!none":
            status = None
        else:
            status = discord.Game(name=playing)
        await self.bot.change_status(game=status)
        await self.bot.say("I'm playing {0}".format(playing))
    
    ## Get an invite to a server the bot is connected to, if possible.
    @commands.command(pass_context=True)
    @prefix('$')
    @botmaster()
    async def inviteme(self, ctx, *, name: str):
        """Get an invite to a server the bot is connected to, if possible."""
        for serv in server_list:
            if serv.name == name:
                try:
                    invite = await self.bot.create_invite(serv.default_channel)
                    await self.bot.send_message(ctx.message.author,
                    "Invite to {0}: {1}".format(name, invite))
                except HTTPException as error:
                    await self.bot.s ay("Error getting invite: {0}"
                    .format(error))
    
    ## Make the bot leave a server
    @commands.command(pass_context=True)
    @prefix('$')
    @botmaster()
    async def leave(self, ctx):
        """Leave the server where this command was received"""
        await self.bot.say("Alright... I understand I'm not wanted here...")
        await self.bot.leave_server(ctx.message.server)
        
def setup(bot):
    bot.add_cog(Botmaster(bot))
