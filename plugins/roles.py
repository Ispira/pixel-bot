import json

from discord import Role, Member
from discord.ext import commands as c
from accounts import level
from helpers import update_db

with open("db/roles.json") as rls:
    roles = json.load(rls)

class Roles:
    """Add assignable roles to your server today!
    
    This plugin allows you to add roles to a list for users to safely assign themselves.
    The target is servers with 'category' roles (such as my gaming server which has 
    roles for every game we support). This plugin allows said servers to let users set
    themselves to whatever combination of roles they choose, rather than having to ask an
    admin or set up a complicated role structure.
    """
    def __init__(self, bot):
        self.bot = bot

    @c.group(aliases=["roles"], pass_context=True, no_pm=True)
    async def role(self, ctx):
        """Role related commands.
        
        Running the command without arguments will display the list of available
        roles in the current server.
        """
        if ctx.invoked_subcommand is None:
            s_id = ctx.message.server.id
            if s_id in roles:
                message = " | ".join(roles[s_id])
                await self.bot.say(f"`{message}`")
            else:
                await self.bot.say("\U00002754 This server has no available roles.")
    
    @role.command(name="get", pass_context=True)
    async def role_get(self, ctx, *, role_name: Role):
        """Get a role."""
        s_id = ctx.message.server.id
        if s_id not in roles:
            await self.bot.say("\U00002754 This server has no available roles.")
            return

        if role_name.name in roles[s_id]:
            await self.bot.add_roles(ctx.message.author, role_name)
            await self.bot.say("\U00002705")
        else:
            await self.bot.say("\U00002754 That role is not assignable.")
    
    @role.command(name="lose", pass_context=True)
    async def role_lose(self, ctx, *, role_name: Role):
        """Remove a role from yourself."""
        s_id = ctx.message.server.id
        if s_id not in roles:
            await self.bot.say("\U00002754 This server has no available roles.")
            return
        
        if role_name.name in roles[s_id]:
            await self.bot.remove_roles(ctx.message.author, role_name)
            await self.bot.say("\U00002705")
        else:
            await self.bot.say("\U00002754 That role is not assignable.")

    @role.command(name="add", pass_context=True)
    @level(2)
    async def role_add(self, ctx, *, role_name: Role):
        """Add an assignable role."""
        s_id = ctx.message.server.id
        if s_id not in roles:
            roles[s_id] = []
        roles[s_id].append(role_name.name)
        update_db(roles, "roles")
        await self.bot.say("\U00002705")
    
    @role.command(name="remove", pass_context=True)
    @level(2)
    async def role_remove(self, ctx, *, role_name: Role):
        """Remove an assignable role."""
        s_id = ctx.message.server.id
        if s_id not in roles:
            await self.bot.say("\U00002757 This server has no assignable roles.")
            return
        roles[s_id].remove(role_name.name)
        if len(roles[s_id]) == 0:
            del roles[s_id]
        update_db(roles, "roles")
        await self.bot.say("\U00002705")
    
    @role.command(name="give")
    @level(2)
    async def role_give(self, member: Member, *, role_name: Role):
        """Give a role to another user.
        
        This command is NOT limited by the assignable roles list, so please use
        caustion when giving roles out. This command is intended to be a shortcut
        for setting users to higher roles than you would normally want available
        through the assignable roles list.
        """
        await self.bot.add_roles(member, role_name)
        await self.bot.say("\U00002705")
    
    @role.command(name="take")
    @level(2)
    async def role_take(self, member: Member, role_name: Role):
        """Take a role from a user.

        This command is NOT limited by the assignable roles list, it will remove ANY
        role from a user.
        """
        await self.bot.remove_roles(member, role_name)
        await self.bot.say("\U00002705")

def setup(bot):
    bot.add_cog(Roles(bot))
