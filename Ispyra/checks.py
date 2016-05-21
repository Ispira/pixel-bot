from discord.ext import commands

from bot_globals import bot_masters, blacklist

#Check if a user is allowed to use a command
#Perm 0 is simply blacklist checking
#Perm 1 also checks if the user is a botmaster
def allowed(perm, pref):
    def permission(ctx):
        uid = ctx.message.author.id
        if perm == 0:
            return uid not in blacklist and pref is ctx.prefix
        elif perm == 1:
            return uid in bot_masters and uid not in blacklist and pref is ctx.prefix
    return commands.check(permission)
