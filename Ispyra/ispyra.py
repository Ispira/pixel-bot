import sys

from discord.ext import commands
from bot_globals import *
from checks import *

#Create the logs and set up the bot
create_log(log_folder, bot_name)
bot = commands.Bot(command_prefix=('|', '^', '$'))
bot.remove_command("help")

#Change the bot's avatar and name if needed
async def update_profile():
    #Avatar
    if os.path.isfile(bot_pic):
        with open(bot_pic, "rb") as image:
            avatar = image.read()
            log_print("Profile image read.")
            try:
                await bot.edit_profile(avatar=avatar)
                log_print("Avatar changed.")
            except discord.InvalidArgument:
                log_print("Avatar not changed: Invalid image file")
    else:
        log_print("Unable to find bot_pic image: {0}. Picture will not be changed"
        .format(bot_pic))
    #Username
    try:
        await bot.edit_profile(username=bot_name)
    except discord.HTTPException as error:
        log_print("Unable to change bot username: {0}"
        .format(error))

#Start up the bot
@bot.event
async def on_ready():
    #Load extensions
    for e in extensions:
        try:
            bot.load_extension(e)
            extensions_loaded.append(e.split('.')[1])
        except Exception as error:
            exc = "{0}: {1}".format(type(error).__name__, error)
            log_print("Failed to load extension {0}, {1}".format(e, exc))

    #Update bot's profile
    await update_profile()
    
    log_print("------------------------STATUS------------------------")
    log_print("Ispyra {0} by Ispira using discord.py by Rapptz"
    .format(version))
    
    log_print("Contributors: {0}"
    .format(' '.join(contributors)))
    
    log_print("Logged in as: {0}"
    .format(bot.user.name))
    
    log_print("With ID: {0}"
    .format(bot.user.id))
    
    log_print("Botmasters: {0}"
    .format(', '.join(bot_masters)))
    
    log_print("Extensions: {0}"
    .format(', '.join(extensions_loaded)))
    
    log_print("Connected to:") 
    for serv in bot.servers:
        log_print("{0},".format(serv.name))
        server_list.append(serv)
    
    log_print("------------------------STATUS------------------------")

## EVENTS ##
@bot.event
async def on_message(message):
    #Log the message unless the config says otherwise
    if log_messages:
        log_print("|{0}|[{1}]<{2}>: {3}"
        .format(message.server, message.channel, message.author, message.content))    
    
    #Don't let the bot do anything with itself
    if message.author == bot.user:
        return
    
    #Handle the command
    await bot.process_commands(message)

@bot.event
async def on_server_join(server):
    #Log it
    log_print("[JOINED] Server: {0}."
    .format(server.name))
    
    #Add to the list of currently connected servers
    if server not in server_list:
        server_list.append(server)

@bot.event
async def on_server_remove(server):
    #Log it
    log_print("[LEFT] Server: {0}"
    .format(server.name))
    
    #Remove the server from the server_list
    if server in server_list:
        server_list.remove(server)

@bot.event
async def on_server_update(before, after):
    #You know the drill by now
    log_print("[EDIT] Server: {0} was updated. {1}"
    .format(before.name, after.name))
    
    #Update the server_list
    if before in server_list:
        server_list.remove(before)
        server_list.append(after)

## COMMANDS ##
## These are considered "Base" commands that will always work
## Regardless of loaded extensions
## Load extensions
@bot.command(pass_context=True)
@allowed(1, '$')
async def load(ctx, name: str):
    try:
        bot.load_extension("extensions.{0}".format(name))
        extensions_loaded.append(name)
        await bot.say("Loaded {0}.".format(name))
    except Exception as error:
        exc = "{0}: {1}".format(type(error).__name__, error)
        log_print("Failed to load extension {0}"
        .format(name, exc))

## Unload extensions
@bot.command(pass_context=True)
@allowed(1, '$')
async def unload(ctx, name: str):
    bot.unload_extension("extensions.{0}".format(name))
    await bot.say("Unloaded {0}.".format(name))

bot.run(bot_token)
sys.exit(0)
