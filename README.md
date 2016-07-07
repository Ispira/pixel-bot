# **Ispyra**
#### A discord bot utilizing [discord.py](https://github.com/Rapptz/discord.py) 
---
##### **Command prefixes:** *(Note that these might not be the same for unofficial extensions)*
##### USER commands are prefixed with a vertical pipe: `|`. Anyone can use them.
##### ADMIN commands are prefixed with a dollar sign: `$`. They require botmaster, or special permissions.
###### Log files will by default be created in a folder named `logs` beside the ispyra.py file.

## **Installation**:
***Prerequisites:***

 - [Python 3.5+](https://www.python.org/downloads/) (In the future you will NEED 3.6 or strings will be fucked)
 - [discord.py](https://github.com/Rapptz/discord.py)
 - [Bot Account/App](https://discordapp.com/developers/applications/) (This but is not made to be a self bot, so email login is not an option)
 - [Imgur API App](https://api.imgur.com/#registerapp) (Required for the `imgur` extension)
 - [ImgurPython](https://github.com/Imgur/imgurpython) (Required for the `imgur` extension)
 - [python-xkcd](https://pypi.python.org/pypi/xkcd/) (Required for the `user` extension)
 - Windows or Linux. It should run fine on OS X or else that runs Python 3.5 but it is NOT supported.

***Download the bot:***

 - Using git: `git clone https://github.com/Ispira/Ispyra.git`
 - Direct Download: `https://github.com/Ispira/Ispyra/archive/master.zip`
 
***Configure and launch the bot:***

 - Edit `config.ini` in the `config` folder to set the bot up
   - Edit any extra configs in the `extensions/extension` folder(s). Such as `extensions/imgur/config.txt` with the correct information
 - Add botmasters by user ID to `config/botmasters.txt`
 - Add blacklisted user ID to `config/blacklist.txt`
 - Launch the bot:
	 - `python ispyra.py` or
	 - `python3 ispyra.py` depending on your operating system.

## **Commands:**
New docs coming soon(tm).