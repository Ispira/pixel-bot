import sys
import os
import logging
import json
import discord

from datetime import datetime
from discord.ext import commands as c

# Assorted things
date = datetime.now()

# Get the config
with open("config/config.json") as js:
    config = json.load(js)

# Set up the config values
token      = config["token"]
bot_name   = config["bot_name"]
bot_avatar = config["bot_avatar"]
prefix     = config["command_prefix"]
version    = config["version"]
log_file   = config["log_file"]

# Set up logging
log_file = "logs/{0.year}-{0.month}-{0.day}-{0.hour}-{0.minute}_{1}".format(date, log_file)
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
bot = c.Bot(command_prefix=prefix, pm_help=True, description=description)

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
    
    # Log bot status
    log.info("------------------------STATUS------------------------")
    log.info(f"{date}")
    log.info(f"Ispyra v{version}")
    log.info(f"Logged in as {bot.user.name}")
    log.info("Botmasters: []")
    log.info("Plugins: []")
    log.info("Connected to: []")
    log.info("------------------------STATUS------------------------")

@bot.command()
async def quit():
    await bot.logout()

bot.run(token)
