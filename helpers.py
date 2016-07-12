import sys
import os
import json
import logging

from datetime import datetime
from discord.ext import commands as c

# Get any needed config values
with open("config/config.json") as cfg:
    config = json.load(cfg)

owner    = config["owner"]
config   = None

#### Helper functions

# Take a datetime object and return a prettified string
def pretty_datetime(dt: datetime, display = "FULL"):
    pretty = ""
    if display.upper() == "FULL":
        pretty = f"{dt.year}-{dt.month}-{dt.day} {dt.hour}:{dt.minute}"
    elif display.upper() == "TIME":
        pretty = f"{dt.hour}:{dt.minute}:{dt.second}"
    return pretty

# Create a logging flow and return the logger
def get_logger(file_name):
    date = datetime.now()
    timestamp = "{0.year}-{0.month}-{0.day}_{0.hour}-{0.minute}-{0.second}".format(date)
    log_file = f"logs/{timestamp}_{file_name}"
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.addHandler(logging.FileHandler(filename=file_name, encoding="utf-8"))
    log.addHandler(logging.StreamHandler(sys.stdout))
    return log

# Update a database
def update_db(db, name):
    with open(f"db/{name}.json", "w") as dbfile:
        json.dump(db, dbfile, indent=4)

#### Checks

# Command check returning if the user is the bot owner or not
def is_owner():
    return c.check(lambda ctx: ctx.message.author.id == owner)
