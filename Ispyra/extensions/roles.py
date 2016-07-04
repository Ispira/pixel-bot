#Role extensions v1.0.0
#Yeah the code is a bit off, the whole bot is about to be rewritten.
from discord.ext import commands
from checks import prefix, permission
import discord
from discord.utils import find

class Roles():
    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = []
        #Roles do NOT perisist currently, they will after the rewrite
        #I just REALLY needed this for my server and don't feel like manually copying it
    
    ## Role management
    @commands.group(pass_context=True)
    @prefix('|')
    async def role(self, ctx):
        """Role related commands."""
        if ctx.invoked_subcommand is None:
            await bot.say("Usage: `role <get | lose> [args]`")
    
    @role.command(pass_context=True)
    @prefix('|')
    async def list(self, ctx):
        """List of roles you can add to yourself."""
        msg = ""
        for s, r in self.allowed_roles:
            if s == ctx.message.server:
                msg += "{0}, ".format(r.name)
        await self.bot.say("Allowed roles: `{0}`".format(msg))

    @role.command(pass_context=True)
    @prefix('|')
    async def get(self, ctx, role: str):
        """Add a role to yourself."""
        role = find(lambda r: r.name == role, ctx.message.server.roles)
        if (ctx.message.server, role) in self.allowed_roles:
            await self.bot.add_roles(ctx.message.author, role)
            await self.bot.say("You are now a member of {0}.".format(role.name))
        else:
            await self.bot.say("That role is not allowed, or doesn't exist. Try `|role list`")
    
    @role.command(pass_context=True)
    @prefix('|')
    async def lose(self, ctx, role: str):
        """Remove a role from yourself."""
        role = find(lambda r: r.name == role, ctx.message.server.roles)
        if role in ctx.message.author.roles:
            await self.bot.remove_roles(ctx.message.author, role)
            await self.bot.say("You are no longer a memeber of {0}.".format(role.name))
        else:
            await self.bot.say("You are not a member of {0}.".format(role.name))
    
    ## Add/Remove self-assignable roles
    @commands.command(pass_context=True)
    @permission(manage_server=True)
    @prefix('$')
    async def addrole(self, ctx, role: discord.Role):
        """Add a role for users to assign to themselves."""
        self.allowed_roles.append((ctx.message.server, role))
        await self.bot.say("Role added.")
    
    @commands.command(pass_context=True)
    @permission(manage_server=True)
    @prefix('$')
    async def remrole(self, ctx, role: discord.Role):
        """Remove a role for users to assign to themselves."""
        self.allowed_roles.remove((ctx.message.server, role))
        await self.bot.say("Roel removed.")

def setup(bot):
    bot.add_cog(Roles(bot))