#Group extension v1.0.0
from discord.ext import commands
from discord import ChannelType
from checks import prefix
import asyncio

class Group():
    def __init__(self, bot):
        self.bot = bot
        self.channels = []
    
    ## Private channel creation
    @commands.group(pass_context=True)
    @prefix('|')
    async def group(self, ctx):
        """Create group channels."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Usage: `|group <create | clear>`")

    @group.command(pass_context=True)
    async def create(self, ctx):
        """Create a group channel."""
        name = str(ctx.message.author.discriminator)
        try:
            channel = await self.bot.create_channel(ctx.message.server, "Group_" + name, type=ChannelType.voice)
            await self.bot.say("Channel {0} created.".format(name))
        except:
            await self.bot.say("There was a problem...")
            return
        self.channels.append(channel.id)
    
    @group.command(pass_context=True)
    async def clear(self, ctx):
        """Remove empty group channels."""
        for channel in self.channels[:]:
            chan = ctx.message.server.get_channel(channel)
            if len(chan.voice_members) == 0:
                try:
                    await self.bot.delete_channel(chan)
                    self.channels.remove(channel)
                    await asyncio.sleep(0.25)
                except:
                    await self.bot.say("There was a problem deleting {0}...".format(chan.name))

def setup(bot):
    bot.add_cog(Group(bot))
