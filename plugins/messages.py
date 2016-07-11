from discord import Channel
from discord.ext import commands as c
from accounts import level

class Messages:
    """Message management plugin.
    
    The star of the show is message cross-posting and moving, but this plugin handles
    pinning as well.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @c.command(name="xpost", asliases=["crosspost"], pass_context=True, no_pm=True)
    @level(1)
    async def x_post(self, ctx, message: str, destination: Channel):
        """Cross-posts a message to another channel."""
        message = await self.bot.get_message(ctx.message.channel, message)
        header = f"{message.author.mention} ({message.channel.mention}):"
        await self.bot.send_message(destination, f"{header}\n{message.content}")
        await self.bot.say("\U00002705")
    
    @c.command(name="move", pass_context=True, no_pm=True)
    @level(1)
    async def move_post(self, ctx, message: str, destination: Channel):
        """Move a message to a different channel."""
        message = await self.bot.get_message(ctx.message.channel, message)
        here = destination.mention
        header = f"{message.author.mention} ({message.channel.mention} -> {here}):"
        await self.bot.send_message(destination, f"{header}\n{message.content}")
        await self.bot.delete_message(message)
        await self.bot.say("\U00002705")
    
    @c.group(pass_context=True)
    @level(1)
    async def pin(self, ctx):
        """Pin or unpin a message."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("What do you expect me to pin? The tail on a donkey?")
    
    # Helper function to pin/unpin messages
    async def do_pinning(self, message_id, channel, pin=True):
        message = await self.bot.get_message(channel, message_id)
        if pin:
            await self.bot.pin_message(message)
        else:
            await self.bot.unpin_message(message)

    @pin.command(name="add", pass_context=True)
    async def pin_add(self, ctx, message: str):
        await self.do_pinning(message, ctx.message.channel)
        await self.bot.say("\U00002705")
    
    @pin.command(name="remove", pass_context=True)
    async def pin_remove(self, ctx, message: str):
        await self.do_pinning(message, ctx.message.channel, False)
        await self.bot.say("\U00002705")

def setup(bot):
    bot.add_cog(Messages(bot))
