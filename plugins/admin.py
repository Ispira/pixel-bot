import asyncio
import json
import discord

from discord.ext import commands as c

class Admin:
    def __init__(self, bot):
        self.bot = bot
