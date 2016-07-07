#Botmaster commands v1.0.0
from discord.ext import commands
import discord
from bot_globals import server_list
from checks import prefix, botmaster, blacklist

class Botmaster():
    def __init__(self, bot):
        self.bot = bot
    
    ## List names of currently connected servers
    @commands.command()
    @prefix('|')
    @botmaster()
    async def servers(self):
        """List the names of all currently connected servers."""
        server_names = []
        for serv in server_list:
            server_names.append(serv.name)
        await self.bot.say(" | ".join(server_names))
    
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
    
    ## Add/remove a user from the blacklist
    @commands.group(pass_context=True)
    @prefix('$')
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

def setup(bot):
    bot.add_cog(Botmaster(bot))
