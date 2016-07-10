import asyncio
import json

from discord import Member, Role
from discord.ext import commands as c
from accounts import level

with open("plugins/settings/admin.json") as cfg:
    config = json.load(cfg)

class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(config["channel"])
        self.log = config["log"]
        self.display_purges = config["display_purges"]
    
    # Helper function for logging
    async def log_to_channel(self, author, target, log_type, info):
        if self.log:
            author = f"{author.name}#{author.discriminator}"
            target = f"{target.name}#{target.discriminator}"
            header = f"**[{log_type}]** *by {author}*"
            body = f"**Member:** {target}\n**Reason:** {info}"
            await self.bot.send_message(self.channel, f"{header}\n{body}")

    @c.command(no_pm=True, pass_context=True)
    @level(2)
    async def kick(self, ctx, member: Member, *, reason: str = ""):
        """Kick a member."""
        await self.bot.kick(member)
        await self.bot.say("\U00002705")
        await self.log_to_channel(ctx.message.author, member, "KICK", reason)
    
    @c.command(no_pm=True, pass_context=True)
    @level(2)
    async def ban(self, ctx, member: Member,
        purge: int = 7, *, reason: str = ""):
        """Ban a member."""
        await self.bot.ban(member, purge)
        await self.bot.say("\U00002705")
        await self.log_to_channel(ctx.message.author, member,
            "\U0001F528BAN\U0001F528", reason)
    
    @c.command(no_pm=True, pass_context=True)
    @level(2)
    async def unban(self, ctx, uid: str, *, reason: str = ""):
        """Unban a member by UID."""
        for banned in await self.bot.get_bans(ctx.message.server):
            if banned.id == uid:
                user = banned
                break
        await self.bot.unban(ctx.message.server, user)
        await self.bot.say("\U00002705")
        await self.log_to_channel(ctx.message.author, user, "UNBAN", reason)
    
    @c.command(no_pm=True, pass_context=True)
    @level(2)
    async def softban(self, ctx, member: Member,
        purge: int = 1, *, reason: str = ""):
        """Softban (ban then unban) a member."""
        await self.bot.ban(member, purge)
        await self.bot.unban(member.server, member)
        await self.bot.say("\U00002705")
        await self.log_to_channel(ctx.message.author, member,
            "\U0001F528SOFTBAN\U0001F528", reason)
    
    @c.command(no_pm=True)
    @level(2)
    async def mute(self, member: Member, switch: bool = True):
        """Mute or unmute a member."""
        await self.bot.server_voice_state(member, mute=switch)
        await self.bot.say("\U00002705")
    
    @c.command(no_pm=True)
    @level(2)
    async def deafen(self, member: Member, switch: bool = True):
        """Deafen or undeafen a member."""
        await self.bot.server_voice_state(member, deafen=switch)
        await self.bot.say("\U00002705")
    
    # Message purging helper function
    async def purge_messages(self, location, message, limit, check):
        removed = await self.bot.purge_from(message.channel, limit=limit,
            before=message, check=check)
        # Display information about the purge
        if self.display_purges:
            await self.bot.say("\U00002705 {0} message(s) purged from {1}."
                .format(len(removed), location))

    @c.group(pass_context=True)
    @level(1)
    async def purge(self, ctx):
        """Purge messages."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("\U00002754 What should be purged?")
    
    @purge.command(name="all", aliases=["everyone", pass_context=True)
    async def purge_all(self, ctx, amount: int):
        """Purge messages from everyone."""
        await self.purge_messages("everyone", ctx.message, amount,
            lambda m: m is not None)

    @purge.command(name="user", aliases=[]"member"], pass_context=True)
    async def purge_member(self, ctx, member: Member, amount: int):
        """Purge messages from a member."""
        await self.purge_messages(f"{member.mention}", ctx.message, amount,
            lambda m: m.author.id == member.id)
    
    @purge.command(name="id", aliases=["uid"], pass_context=True)
    async def purge_uid(self, ctx, uid: str, amount: int):
        """Purge messages by UID."""
        await self.purge_messages(uid, ctx.message, amount,
            lambda m: m.author.id == uid)
    
    @purge.command(name="role", aliases=["group"], pass_context=True)
    async def purge_role(self, ctx, role: Role, amount: int):
        """Purge messages from a role."""
        await self.purge_messages(f"{role.name}", ctx.message, amount,
            lambda m: role in m.author.roles)

def setup(bot):
    bot.add_cog(Admin(bot))
