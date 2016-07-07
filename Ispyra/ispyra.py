import sys
import asyncio

from io import StringIO
from discord.ext import commands
from bot_globals import *
from checks import *

#Create the logs and set up the bot
create_log(log_folder, bot_name)
bot = commands.Bot(command_prefix='|', pm_help=True)
first_ready = True

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
    if not first_ready:
        log_print("[RESUME] Bot resumed connection.")
        return
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
        log_print("[{0}] - #{1} <{2}>: {3}"
        .format(message.server, message.channel, message.author, message.content))    
    
    #Don't let the bot do anything with itself
    if message.author == bot.user:
        return
    
    #Handle the command
    await bot.process_commands(message)

@bot.event
async def on_command(command, ctx):
    #Handle logging commands
    destination = None
    if ctx.message.channel.is_private:
        destination = "DM"
    else:
        destination = "[{0.server.name}] #{0.channel.name}".format(ctx.message)
    
    if log_commands:
        log_print("Command `{0.content}` issued by `{0.author}` in: {1}"
        .format(ctx.message, destination))

@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(channel, "That command cannot be used in DMs")
    elif isinstance(error, commands.DisabledCommand):
        pass
    elif isinstance(error, commands.CheckFailure):
        await bot.send_message(channel, "I'm afraid I can't do that...")
    elif isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(channel, "Missing argument(s).")

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
## Completely exit the bot
@bot.command()
@allowed()
@is_owner()
async def quit():
    """Completely closes the bot."""
    await bot.say("Bye...")
    await bot.logout()

## Load extensions
@bot.command(pass_context=True)
@allowed()
@is_owner()
async def load(ctx, name: str):
    """Load an extension."""
    ext_file = "extensions/{0}.py".format(name)
    if os.path.isfile(os.path.abspath(ext_file)):
        try:
            bot.load_extension("extensions.{0}".format(name))
            extensions_loaded.append(name)
            await bot.say("Loaded {0}.".format(name))
        except Exception as error:
            exc = "{0}: {1}".format(type(error).__name__, error)
            log_print("Failed to load extension {0}"
            .format(name, exc))
    else:
        await bot.say("No extension {0} exists.".format(name))

## Unload extensions
@bot.command(pass_context=True)
@allowed()
@is_owner()
async def unload(ctx, name: str):
    """Unload an extension."""
    try:
        if name in extensions_loaded:
            bot.unload_extension("extensions.{0}".format(name))
            extensions_loaded.remove(name)
            await bot.say("Unloaded {0}.".format(name))
        else:
            await bot.say("No extension named {0} is loaded."
            .format(name))
    except Exception as error:
        exc = "{0}: {1}".format(type(error).__name__, error)
        log_print("Failed to unload extension {0}"
        .format(name, exc))

## Eval command for debugging
#You'll need to set enabled=True for this to work
#But don't do that
@bot.command(pass_context=True, hidden=True, enabled=False)
@allowed()
@is_owner()
async def ev(ctx, *, code: str):
    """Extremely unsafe eval command."""
    code = code.strip("` ")
    python = "```python\n{0}\n```"
    result = None
    
    try:
        result = eval(code)
        if asyncio.iscoroutine(result):
            result = await result
    except Exception as error:
        await bot.say(python.format(type(error).__name__ + ': ' + str(error)))
        return
    
    await bot.say(python.format(result))

## Exec command because I'm a madman
#If you enable this one you're equally as insane as I am
#I both respect you, and fear you for that
@bot.command(pass_context=True, hidden=True, enabled=False)
@allowed()
@is_owner()
async def ex(ctx, *, code: str):
    """The death command"""
    code = code.strip("```").lstrip("py")
    code += "import asyncio\nloop = asyncio.get_event_loop"
    python = "```python\n{0}\n```"
    result = None
    env = {}
    env.update(locals())
    stdout = sys.stdout
    redirect =  sys.stdout = StringIO()

    try:
        exec(code, globals(), env)
    except Exception as error:
        await bot.say(python.format(type(error).__name__ + ": " + str(error)))
    finally:
        sys.stdout = stdout
    
    await bot.say(python.format(redirect.getvalue()))

bot.run(bot_token)
