import asyncio
import json

from discord import ChannelType
from discord.ext import commands as c

# Get the config
with open("plugins/settings/groups.json") as cfg:
    config = json.load(cfg)

# Grab the group database
with open("db/groups.json") as grps:
    groups = json.load(grps)

# Helper function for updating database
def update_db(db):
    with open("db/groups.json", "w") as grps:
        json.dump(db, grps, indent=4)

# Helper function to delete channels
# This feels like an abomination
async def clear_channels(bot, location = None):
    for chan in groups["channels"][:]:
        channel = bot.get_channel(chan)
        if len(channel.voice_members) == 0:
            try:
                await bot.delete_channel(channel)
                groups["channels"].remove(chan)
                await asyncio.sleep(0.25)
            except:
                groups["channels"].remove(chan)
                if location is None:
                    continue
                await bot.send_message(location,
                    f"\U00002757 Unable to delete channel {channel.name}")
    if location is None:
        return
    update_db(groups)

class Groups:
    def __init__(self, bot):
        self.bot = bot
        self.prefix = config["prefix"]
        self.suffix = config["suffix"]
    
    @c.group(no_pm=True, pass_context=True)
    async def group(self, ctx):
        """Create group channels.
        
        Running the command without arguments will clear empty channels.
        """
        if ctx.invoked_subcommand is None:
            await clear_channels(self.bot, ctx.message.channel)
            await self.bot.say("\U00002705 Cleared empty channels.")
    
    @group.command(pass_context=True)
    async def create(self, ctx, *, name: str = None):
        """Create a group channel."""
        if name is None:
            name = ctx.message.author.discriminator
        name = f"{self.prefix}{name}{self.suffix}"
        try:
            channel = await self.bot.create_channel(ctx.message.server, name,
                type=ChannelType.voice)
            await self.bot.say("\U00002705 Channel created.")
            groups["channels"].append(channel.id)
            update_db(groups)
        except:
            await self.bot.say("\U00002757")

def setup(bot):
    bot.add_cog(Groups(bot))
