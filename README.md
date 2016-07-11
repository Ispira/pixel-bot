# **Ispyra**
#### A discord bot utilizing [discord.py](https://github.com/Rapptz/discord.py) 
---
# THIS IS THE DEV VERSION
# IT WON'T WORK HALF THE TIME
# DON'T USE IT
# PLEASE
# STOP ASKING ME ABOUT IT
# NO
# GO AWAY

## **Setup**
***Warning:*** This bot is made mainly for my specific server(s). No attempt is, or will ever
be made to make installation or setup easier. This bot uses dev builds of discord.py and even Python itself.

***Prerequisites:***
- [Python 3.6](https://www.python.org/download/pre-releases/)
  - Python 3.6 is REQUIRED as this bot makes heavy use of the new string formatting.
- [discord.py](https://github.com/Rapptz/discord.py)
  - Latest development version
- [Discord API app](https://discordapp.com/developers/applications/me)
  - You'll need to create the bot account for the app if that wasn't obvious.
- [imgurpython](https://github.com/Imgur/imgurpython)
- [Imugr API app](http://api.imgur.com/)

***Setup:***
- Download or clone the repo
- Edit `config/config.json` with the appropriate info and settings
- Edit config files in `plugins/settings` with the appropriate settings
  - Do **NOT** edit files in the `db` folder yourself. They will be updated by the bot.
- Launch the bot via `python bot.py` or `python3 bot.py` depending on your system
  - If the bot can't create folders or files it'll complain because it needs to do that
  - If you're on windows run the command `chcp 65001` before starting the bot else you'll get errors for days
