#Admin commands v2.1.1
import discord
import asyncio
from discord.ext import commands

from bot_globals import display_purges, server_list
from checks import *

class Admin():
    def __init__(self, bot):
        self.bot = bot

    ## Kick user
    @commands.command()
    @prefix('$')
    @permission(kick_members=True)
    async def kick(self, member: discord.Member):
        """Kick a user."""
        await self.bot.kick(member)
    
    ## Ban user
    @commands.command()
    @prefix('$')
    @permission(ban_members=True)
    async def ban(self, member: discord.Member, purge: int = 7):
        """Ban a user."""
        await self.bot.ban(member, purge)
    
    ## Unban user
    @commands.command(pass_context=True)
    @prefix('$')
    async def unban(self, ctx, uid: str):
        """Unban a user by UID."""
        for banned in await self.bot.get_bans(ctx.message.server):
            if banned.id == uid:
                user = banned
                break
        await self.bot.unban(ctx.message.server, user)
    
    ## Softban
    @commands.command()
    @prefix('$')
    @permission(ban_members=True)
    async def softban(self, member: discord.Member, purge: int = 1):
        """Softban (ban then unban) a user."""
        server = member.server
        await self.bot.ban(member, purge)
        await self.bot.unban(server, member)

    ## Purge messages
    @commands.group(pass_context=True)
    @prefix('$')
    @permission(manage_messages=True)
    async def purge(self, ctx):
        """Purge messages."""
        #The user is in fact doing it wrong
        if ctx.invoked_subcommand is None:
            await self.bot.say("Usage: `$purge <all | user | role> <target>`")
    
    #Handle the actual purging
    async def purge_messages(self, location, message, limit, check):
        removed = await self.bot.purge_from(message.channel,
        limit=limit, before=message, check=check)
        #Show info about the purge if the config says so
        if display_purges:
            reply = await self.bot.say("{0} message(s) were purged from {1}."
            .format(len(removed), location))
            await asyncio.sleep(4)
            await self.bot.delete_message(reply)
    
    @purge.command(pass_context=True)
    async def all(self, ctx, amt: int):
        """Remove all messages"""
        await self.purge_messages("everyone", ctx.message, amt, lambda e: True)
    
    @purge.command(pass_context=True)
    async def user(self, ctx, member: discord.Member, amt: int = 25):
        """Remove messages from a user"""
        who = member.mention
        await self.purge_messages(who, ctx.message, amt, lambda e: e.author == member)

    @purge.command(pass_context=True)
    async def uid(self, ctx, uid: str, amt: int = 25):
        """Remove messages from a user by UID"""
        await self.purge_messages(uid, ctx.message, amt, lambda e: e.author.id == uid)
    
    @purge.command(pass_context=True)
    async def role(self, ctx, role: discord.Role, amt: int = 25):
        """Remove messages from anyone with the specified role"""
        who = role.mention
        await self.purge_messages(who, ctx.message, amt, lambda e: role in e.author.roles)
    
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
                    await self.bot.say("Error getting invite: {0}"
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
    bot.add_cog(Admin(bot))
