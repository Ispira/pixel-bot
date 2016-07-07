#Message commands v1.0.0
from discord.ext import commands
import discord
from checks import allowed, permission

class Messages():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, no_pm=True)
    @allowed()
    @permission(manage_messages=True)
    async def xpost(self, ctx, message: str, dest: discord.Channel):
        """Cross-posts a message to another channel."""
        message = await self.bot.get_message(ctx.message.channel, message)
        header = "{0} ({1}):\n".format(message.author.mention, message.channel.mention)
        await self.bot.send_message(dest, header + message.content)
    
    @commands.command(pass_context=True, no_pm=True)
    @allowed()
    @permission(manage_messages=True)
    async def move(self, ctx, message: str, dest: discord.Channel):
        """Move a message to a different channel."""
        message = await self.bot.get_message(ctx.message.channel, message)
        header = "{0} ({1} -> {2}):\n".format(message.author.mention, message.channel.mention, dest.mention)
        await self.bot.send_message(dest, header + message.content)
        await self.bot.delete_message(message)
    
    @commands.group(pass_context=True)
    @allowed()
    @permission(manage_messages=True)
    async def pin(self, ctx):
        """Pin or unpin a message."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Usage: `$pin <add | remove> <message ID>`")
    
    #Do the (un)pinning
    async def pin_message(self, mid, chan, pin=True):
        message = await self.bot.get_message(chan, mid)
        if pin:
            await self.bot.pin_message(message)
        else:
            await self.bot.unpin_message(message)
    
    @pin.command(pass_context=True)
    async def add(self, ctx, message: str):
        await self.pin_message(message, ctx.message.channel, True)
    
    @pin.command(pass_context=True)
    async def remove(self, ctx, message: str):
        await self.pin_message(message, ctx.message.channel, False)


def setup(bot):
    bot.add_cog(Messages(bot))
