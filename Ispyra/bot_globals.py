#Global variables and functions for the bot
import configparser
import logging
import os
import sqlite3

#Print to console and log the data
def log_print(data):
    try:
        print(data)
        logging.info(data)
    #The unfortunate end user is on Windows
    except UnicodeEncodeError:
        data = data.encode("utf-8")
        log_print(data)

#Create a log file and set up the logger for it
def create_log(log_folder, file_name, file_number=0):
    name = os.path.abspath("{0}/{1}_{2}.log"
    .format(log_folder, file_name, str(file_number)))
    if not os.path.isfile(name):
        logging.basicConfig(filename=name, level=logging.INFO, format="%(message)s")
        log_print("Log file {0} created.".format(name))
    else:
        file_number += 1
        create_log(log_folder, file_name, file_number)


version = "v1.0.0"

#Extensions
extensions = []
extensions_loaded = []
for e in os.listdir(os.path.abspath("./extensions")):
        if e.endswith(".py"):
            extensions.append("extensions.{0}".format(os.path.splitext(e)[0]))

#List of servers the bot is connected to
server_list = []

#Set up the config
config = configparser.ConfigParser()
config.read(os.path.abspath("./config/config.ini"))

#Everyone who has contributed to the bot
contributors = ["Ispira"]

#Load values from config files
log_messages = config.getboolean("bot_settings", "log_messages")
display_purges = config.getboolean("bot_settings", "display_purges")
bot_token = config["bot_settings"]["token"]
bot_name = config["bot_settings"]["bot_name"]
bot_pic = config["bot_settings"]["bot_pic"]

#File variables
log_folder = os.path.abspath(config["files"]["log_folder"])
database = os.path.abspath(config["files"]["database"])

#Botmasters and blacklist
bot_masters = open(os.path.abspath("./config/botmasters.txt")).readlines()
blacklist = open(os.path.abspath("./config/blacklist.txt")).readlines()

#Connect to the database and make sure the matchmaking table exists
db = sqlite3.connect(database)
db.execute("""CREATE TABLE IF NOT EXISTS mm
(id INTEGER, user TEXT, game TEXT, subgame TEXT, gsize INTEGER, need INTEGER, contact TEXT, timer REAL)""")
