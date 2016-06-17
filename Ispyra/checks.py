from discord.ext import commands

from bot_globals import bot_owner, bot_masters, blacklist

#Check if the user is the bot's owner
def owner(uid):
    return uid == bot_owner

def is_owner():
    return commands.check(lambda ctx: owner(ctx.message.author.id))

#Check the command prefix
#Also checks if the user is blacklisted or not
def prefix(pref):
    def check(ctx):
        if ctx.message.author.id in blacklist:
            return False
        elif ctx.prefix == pref:
            return True
    return commands.check(check)

#Check if the user is a botmaster
def botmaster():
    return commands.check(lambda ctx: ctx.message.author.id in bot_masters)

#Check if the user has permission for the command
def permission(**perms):
    def check(ctx):
        msg = ctx.message
        if perms is None:
            return owner(msg.author.id)
        resolved = msg.channel.permissions_for(msg.author)
        return all(getattr(resolved, name, None) == value for name, value in perms.items())
    return commands.check(check)
