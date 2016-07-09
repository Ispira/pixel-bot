# Bot accounts to handle permissions
# This allows customization to some degree of who can do what
# Much easier than just Discord permissions or botmaster lists
# Currently this just goes off of user id and permission level
# However in the future this will include a login/password system
import json

from discord.ext import commands as c

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
    """Account related commands."""
    def __init__(self, bot):
        self.bot = bot
    
    @c.group(name="account", pass_context=True)
    async def account_command(self, ctx):
        """Check your account level."""
        if ctx.invoked_subcommand is None:
            uid = ctx.message.author.id
            if uid in accounts:
                await self.bot.say("Account level is: {0}".format(accounts[uid]["level"]))
            else:
                await self.bot.say(f"No account with ID {uid} exists.")
    
    @account_command.command(name="add")
    @level(2)
    async def account_add(self, uid: str, lvl: int):
        """Add an account."""
        accounts[uid] = {}
        accounts[uid]["level"] = lvl
        with open("db/accounts.json", "w") as accs:
            json.dump(accounts, accs, indent=4)
        
        await self.bot.say("Account added.")
    
    @account_command.command(name="remove")
    @level(2)
    async def account_remove(self, uid: str):
        """Remove an acconut."""
        if uid not in accounts:
            await self.bot.say(f"No account with ID {uid} exists.")
            return
        
        del accounts[uid]
        with open("db/accounts.json", "w") as accs:
            json.dump(accounts, accs, indent=4)
        
        await self.bot.say("Account removed.")
    
    @account_command.command(name="update")
    @level(2)
    async def account_update(self, uid: str, lvl: int):
        """Update an account."""
        if uid not in accounts:
            await self.bot.say(f"No accounts with ID {uid} exists.")
            return
        
        accounts[uid]["level"] = lvl
        with open("db/accounts.json", "w") as accs:
            json.dump(accounts, accs, indent=4)
        
        await self.bot.say("Account updated.")

def setup(bot):
    bot.add_cog(Accounts(bot))
