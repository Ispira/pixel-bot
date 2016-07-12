# Bot accounts to handle permissions
# This allows customization to some degree of who can do what
# Much easier than just Discord permissions or botmaster lists
# Currently this just goes off of user id and permission level
# However in the future this will include a login/password system
import json

from discord.ext import commands as c
from helpers import update_db

# Grab the config
with open("config/config.json") as cfg:
    owner = json.load(cfg)["owner"]

# Grab the account database
with open("db/accounts.json") as accs:
    accounts = json.load(accs)

def level(required=0):
    def check(ctx):
        uid = ctx.message.author.id
        # Bot owner can always do anything
        if uid == owner:
            return True
        # Account is required otherwise
        elif uid not in accounts:
            return False
        else:
            return accounts[uid]["level"] >= required
    return c.check(check)

class Accounts:
    """Account system.
    
    This system allows users to be granted a permission level which can be used for
    command checks. The 'level' check functionis included for importing to other
    plugs to make life easier. The permission levels are global and apply to all
    servers.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @c.group(aliases=["accounts"], pass_context=True)
    async def account(self, ctx):
        """Add/remove/update accounts.
        
        Running the command without arguments will display your current account level.
        """
        if ctx.invoked_subcommand is None:
            uid = ctx.message.author.id
            if uid in accounts:
                level = accounts[uid]["level"]
                await self.bot.say(f"Account level is: {level}")
            else:
                await self.bot.say("\U00002754 You do not have an account.")
    
    @account.command(name="search", aliases=["lookup"])
    async def account_search(self, uid: str):
        """Look up an account based on user ID."""
        if uid in accounts:
            level = accounts[uid]["level"]
            await self.bot.say(f"{uid} is level {level}.")
        else:
            await self.bot.say(f"{uid} doesn't have an account.")
    
    @account.command(name="add")
    @level(3)
    async def account_add(self, uid: str, level: int):
        """Add an account."""
        if uid in accounts:
            await self.bot.say("\U00002754 Account already exists.")
            return
        accounts[uid] = {}
        accounts[uid]["level"] = level
        update_db(accounts, "accounts")
        await self.bot.say("\U00002705")
    
    @account.command(name="remove")
    @level(3)
    async def account_remove(self, uid: str):
        """Remove an acconut."""
        if uid not in accounts:
            await self.bot.say(f"\U00002754 No account with ID {uid} exists.")
            return
        del accounts[uid]
        update_db(accounts, "accounts")
        await self.bot.say("\U00002705")
    
    @account.command(name="update", aliases=["change", "modify"])
    @level(3)
    async def account_update(self, uid: str, level: int):
        """Change an account's level."""
        if uid not in accounts:
            await self.bot.say(f"\U00002754 No accounts with ID {uid} exists.")
            return
        accounts[uid]["level"] = level
        update_db(accounts, "accounts")
        await self.bot.say("\U00002705")

def setup(bot):
    bot.add_cog(Accounts(bot))
