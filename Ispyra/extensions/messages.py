#Message commands v1.0.0
from discord.ext import commands
import discord
from checks import prefix, permission

class Messages():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @prefix('$')
    @permission(manage_messages=True)
    async def xpost(self, ctx, message: str, dest: discord.Channel):
        """Cross-posts a message to another channel."""
        message = await self.bot.get_message(ctx.message.channel, message)
        header = "{0} ({1}):\n".format(message.author.mention, message.channel.mention)
        await self.bot.send_message(dest, header + message.content)
    
    @commands.command(pass_context=True)
    @prefix('$')
    @permission(manage_messages=True)
    async def move(self, ctx, message: str, dest: discord.Channel):
        """Move a message to a different channel."""
        message = await self.bot.get_message(ctx.message.channel, message)
        header = "{0} ({1} -> {2}):\n".format(message.author.mention, message.channel.mention, dest.mention)
        await self.bot.send_message(dest, header + message.content)
        await self.bot.delete_message(message)

def setup(bot):
    bot.add_cog(Messages(bot))
