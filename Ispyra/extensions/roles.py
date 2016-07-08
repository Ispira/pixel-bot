#Role extensions v1.1.1
from discord.ext import commands
from checks import permission, botmaster
import discord
from discord.utils import find

class Roles():
    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = []
        #Roles do NOT perisist currently, they will after the rewrite
        #I just REALLY needed this for my server and don't feel like manually copying it
    
    ## Role management
    @commands.group(pass_context=True, no_pm=True)
    @allowed()
    async def role(self, ctx):
        """Role related commands."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Usage: `role <get | lose> [args]`")
    
    @role.command(pass_context=True)
    async def list(self, ctx):
        """List of roles you can add to yourself."""
        msg = ""
        for s, r in self.allowed_roles:
            if s == ctx.message.server:
                msg += "{0}, ".format(r.name)
        await self.bot.say("Allowed roles: `{0}`".format(msg))

    @role.command(pass_context=True)
    async def get(self, ctx, *, role: str):
        """Add a role to yourself."""
        role = find(lambda r: r.name == role, ctx.message.server.roles)
        if (ctx.message.server, role) in self.allowed_roles:
            await self.bot.add_roles(ctx.message.author, role)
            await self.bot.say("You are now a member of {0}.".format(role.name))
        else:
            await self.bot.say("That role is not allowed, or doesn't exist. Try `|role list`")
    
    @role.command(pass_context=True)
    async def lose(self, ctx, *, role: str):
        """Remove a role from yourself."""
        role = find(lambda r: r.name == role, ctx.message.server.roles)
        if role in ctx.message.author.roles:
            await self.bot.remove_roles(ctx.message.author, role)
            await self.bot.say("You are no longer a member of {0}.".format(role.name))
        else:
            await self.bot.say("You are not a member of {0}.".format(role.name))
    
    @role.command(pass_context=True)
    @botmaster()
    async def add(self, ctx, *, role: str):
        """Add an assignable role."""
        role = find(lambda r: r.name == role, ctx.message.server.roles)
        self.allowed_roles.append((ctx.message.server, role))
        await self.bot.say("Role added.")
    
    @role.command(pass_context=True)
    @botmaster()
    async def remove(self, ctx, *, role: str):
        """Remove an assignable role."""
        role = find(lambda r: r.name == role, ctx.message.server.roles)
        self.allowed_roles.remove((ctx.message.server, role))
        await self.bot.say("Role removed.")

def setup(bot):
    bot.add_cog(Roles(bot))