import sys
import os
import asyncio
import logging
import json
import discord

from io import StringIO
from datetime import datetime
from discord.ext import commands as c
from accounts import level

# Assorted things
date = datetime.now()

# Get the configs
with open("config/config.json") as cfg:
    config = json.load(cfg)
with open("db/blacklist.json") as bl:
    blacklist = json.load(bl)

# Set up the config values
owner        = config["owner"]
token        = config["token"]
bot_name     = config["bot_name"]
bot_avatar   = config["bot_avatar"]
prefix       = config["command_prefix"]
log_file     = config["log_file"]
log_messages = config["log_messages"]
log_commands = config["log_commands"]
version      = config["version"]

# Set up logging
timestamp = "{0.year}-{0.month}-{0.day}_{0.hour}-{0.minute}-{0.second}".format(date)
log_file = f"logs/{timestamp}_{log_file}"
if not os.path.exists("logs"):
    os.makedirs("logs")

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler(filename=log_file, encoding="utf-8"))
log.addHandler(logging.StreamHandler(sys.stdout))

# Set the bot up
description="""
General purpose chat and administration bot.
"""
bot = c.Bot(c.when_mentioned_or(prefix), pm_help=True, description=description)
plugins = []

# Events
@bot.event
async def on_ready():
    # Set the bot's name and avatar
    if os.path.isfile(f"logs/{bot_avatar}"):
        with open(bot_avatar, "rb") as avatar:
            try:
                await bot.edit_profile(username=bot_name, avatar=avatar.read())
                log.info("Bot profile updated.")
            except discord.InvalidArgument:
                log.warning("Invalid image file for bot_avatar.")
            except discord.HTTPException as error:
                log.warning(f"Unabled to update bot profile: {error}")
    
    # Load the account commands
    bot.load_extension("accounts")

    # Status header
    log.info("------------------------STATUS------------------------")
    log.info(f"{date}")
    log.info(f"Ispyra v{version}")
    log.info(f"Logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    log.info("------------------------STATUS------------------------")

@bot.event
async def on_message(msg):
    # Log it
    if log_messages:
        log.info(f"[{msg.server} - #{msg.channel}] <{msg.author}>: {msg.content}")
    # Handle the commands
    await bot.process_commands(msg)

@bot.event
async def on_command(cmd, ctx):
    # Log it home skittle
    if log_commands:
        command = f"{ctx.message.content}"
        user = f"{ctx.message.author}#{ctx.message.author.discriminator}"
        location = f"[{ctx.message.server}] - #{ctx.message.channel}"
        log.info(f'[COMMAND] `{command}` by `{user}` in `{location}`')

@bot.event
async def on_command_error(err, ctx):
    channel = ctx.message.channel
    if isinstance(err, c.NoPrivateMessage):
        await bot.send_message(channel, "This command is not available in DMs.")
    elif isinstance(err, c.CheckFailure):
        await bot.send_message(channel, "I'm sorry, I'm afraid I can't do that.")
    elif isinstance(err, c.MissingRequiredArgument):
        await bot.send_message(channel, "Missing argument(s).")
    elif isinstance(err, c.DisabledCommand):
        pass

@bot.event
async def on_server_join(srv):
    log.info(f"[JOIN] {srv.name}")

@bot.event
async def on_server_remove(srv):
    log.info(f"[LEAVE] {srv.name}")

# Global check for all commands
@bot.check
def allowed(ctx):
    return ctx.message.author.id not in blacklist["users"]
# Built-in check for the bot's owner
def is_owner():
    return c.check(lambda ctx: ctx.message.author.id == owner)

# Built-in commands
# Step the bot
@bot.command(name="quit")
@is_owner()
async def quit_bot():
    """Shut the bot down."""
    await bot.say("Shutting down.")
    await bot.logout()

@bot.group(pass_context=True)
async def plugin(ctx):
    """List loaded plugins."""
    if ctx.invoked_subcommand is None:
        await bot.say(" | ".join(plugins))

@plugin.command(name="load")
@is_owner()
async def plugin_load(name: str):
    """Load a plugin."""
    if name in plugins:
        await bot.say(f"Plugin {name} is already loaded.")
        return
    
    if not os.path.isfile(f"plugins/{name}.py"):
        await bot.say(f"No plugin {name} exists.")
        return
    
    try:
        bot.load_extension(f"plugins.{name}")
        plugins.append(name)
        await bot.say(f"Plugin {name} loaded.")
    except:
        await bot.say(f"Error loading {name}.")

@plugin.command(name="unload")
@is_owner()
async def plugin_unload(name: str):
    """Unload a plugin."""
    if name not in plugins:
        await bot.say(f"Plugin {name} is not loaded.")
        return
    
    try:
        bot.unload_extension(f"plugins.{name}")
        plugins.remove(name)
        await bot.say(f"Plugin {name} unloaded.")
    except:
        await bot.say(f"Error unloading {name}.")

@bot.command(name="eval", hidden=True, pass_context=True, enabled=False)
@is_owner()
async def evaluate(ctx, *, code: str):
    """Extremely unsafe eval command."""
    python = "```py\n{0}\n```"
    code = code.strip("` ")
    result = None
    try:
        result = eval(code)
        if asyncio.iscoroutine(result):
            result = await result
    except Exception as err:
        await bot.say(python.format(type(err).__name__ + ": " + str(error)))
        return
    
    await bot.say(python.format(result))

@bot.command(name="exec", hidden=True, pass_context=True, enabled=False)
@is_owner()
async def execute(ctx, *, code: str):
    """If you thought eval was dangerous, wait'll you see exec!"""
    code = code.strip("```").lstrip("py")
    result = None
    env = {}
    env.update(locals())
    stdout = sys.stdout
    redirect = sys.stdout = StringIO()
    
    try:
        exec(code, globals(), env)
    except Exception as err:
        await bot.say(python.format(type(err).__name__ + ": " + str(error)))
    finally:
        sys.stdout = stdout
    
    await bot.say(f"```\n{redirect.getvalue()}\n```")

bot.run(token)
