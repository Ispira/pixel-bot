#Botmaster commands v1.2.1
from discord.ext import commands
import discord
from bot_globals import server_list, bot_masters
from checks import botmaster, blacklist

class Botmaster():
    def __init__(self, bot):
        self.bot = bot
    
    ## List names of currently connected servers
    @commands.command()
    @botmaster()
    async def servers(self):
        """List the names of all currently connected servers."""
        server_names = []
        for serv in server_list:
            server_names.append(serv.name)
        await self.bot.say(" | ".join(server_names))
    
    ## Change the bot's status
    @commands.command()
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
    @botmaster()
    async def invite(self, ctx, *, name: str):
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
    @commands.command(pass_context=True, no_pm=True)
    @botmaster()
    async def leave(self, ctx):
        """Leave the server where this command was received"""
        await self.bot.say("Alright... I understand I'm not wanted here...")
        await self.bot.leave_server(ctx.message.server)
    
    ## Add/remove a user from the blacklist
    @commands.group(pass_context=True)
    @botmaster()
    async def blacklist(self, ctx):
        """Add or remove a user from the blacklist"""
        if ctx.invoked_subcommand is None:
            await self.bot.say(str(blacklist))
    
    @blacklist.command()
    async def add(self, uid: str):
        """Add a user to the bot's blacklist"""
        if uid in blacklist:
            await self.bot.say("User already blacklisted.")
            return
        blacklist.append(uid)
        uid += "\n"
        with open("./config/blacklist.txt", "a") as bl:
            bl.write(uid)
        await self.bot.say("User blacklisted.")
    
    @blacklist.command()
    async def remove(self, uid: str):
        """Remove a user from the blacklist"""
        if uid in blacklist:
            blacklist.remove(uid)
            lines = "\n".join(blacklist)
            with open("./config/blacklist.txt", "w") as bl:
                bl.write("\n")
                bl.writelines(lines)
            await self.bot.say("User removed from blacklist.")
        else:
            await self.bot.say("User not in blacklist.")
    
    ## Add/remove botmasters
    @commands.group(pass_context=True)
    @botmaster()
    async def botmasters(self, ctx):
        """Add or remove a botmaster"""
        if ctx.invoked_subcommand is None:
            await self.bot.say(str(bot_masters))
    
    @botmasters.command(name="add")
    async def _add(self, uid: str):
        """Add a botmaster"""
        if uid in bot_masters:
            await self.bot.say("User is already a botmaster.")
            return
        bot_masters.append(uid)
        uid += "\n"
        with open("./config/botmasters.txt", "w") as bm:
            bm.write(uid)
        await self.bot.say("Botmaster added.")
    
    @botmasters.command(name="remove")
    async def _remove(self, uid: str):
        """Remove a botmaster"""
        if uid in bot_masters:
            bot_masters.remove(uid)
            lines = "\n".join(bot_masters)
            with open("./config/botmasters.txt", "w") as bm:
                bm.write("\n")
                bm.writelines(lines)
            await self.bot.say("Botmaster removed.")
        else:
            await self.bot.say("User is not a botmaster")

def setup(bot):
    bot.add_cog(Botmaster(bot))
