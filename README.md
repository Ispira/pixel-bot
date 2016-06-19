# **Ispyra**
#### A discord bot utilizing [discord.py](https://github.com/Rapptz/discord.py) 
---
##### **Command prefixes:** *(Note that these might not be the same for unofficial extensions)*
##### USER commands are prefixed with a vertical pipe: `|`. Anyone can use them.
##### ADMIN commands are prefixed with a dollar sign: `$`. They require botmaster, or special permissions.
###### Log files will by default be created in a folder named `logs` beside the ispyra.py file.

## **Installation**:
***Prerequisites:***

 - [Python 3.5](https://www.python.org/downloads/)
 - [discord.py](https://github.com/Rapptz/discord.py)
 - [Bot Account/App](https://discordapp.com/developers/applications/) (This but is not made to be a self bot, so email login is not an option)
 - [Imgur API App](https://api.imgur.com/#registerapp) (Required for the `imgur` extension)
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
All commands assume the bot has the permission on the server to do so (Duh).
***Built-In***

 - `|help` Shows help for all user commands.
 - `$help` Shows help for all admin commands.
 - `$load <extension>` Attemps to load `<extension>` if available.
    - Bot owner only.
 - `$unload <extension>` Attemps to unload `<extension>`.
    - Bot owner only.
 - `$quit` Closes the bot completely.
    - Bot owner only.
 - ```$ev `expression` ``` Evaluates the python `expression`. The expression MUST be enclosed in backticks: ``` ` ```, and MUST BE UNCOMMENTED at the bottom of `ispyra.py`!)
    - Bot owner only.

***User Commands*** *(Extension: user)*

 - `|xkcd [number]` Displays the latest XKCD. If `[number]` is specified it will show that specific comic.
    - If `[number]` is `-1` it will diplay a random comic.
 - `|ping` Pong...
 - `|info` Displays bot information including current version.
 - `|status` Displays amount of servers the bot is connected to, and how many botmasters are configured.
 - `|servers` Displays the list of servers (names only) that the bot is connected to.

***Botmaster Commands:*** *(Extension: botmaster)*

 - `$purge <amount> <all | user @User | role @Role>` Iterates through messages and deletes any that fit the arguments.
    - You (and the bot) must have the "Manage Messages" permission.
	- `$purge 5 all` will delete ALL of the last 5 messages.
	- `$purge 5 user @User` will delete any messages that the user you `@Mention`'d sent within the last 5 messages.
	- `$purge 5 role @Role` will delete any messages that the role you  `@Mention`'d sent within the last 5 messages.
 - `$nick @User <name>` Changes the `@Mention`'d user's nickname on the current server to `<name>`.
    - You (and the bot) must have the "Manage Nicknames" permission.
	- Use `!none` as `<name>` to *remove* a nickname.
 -  `$playing <status>` Sets the bot's "Playing:" status on discord to `<status>`
 	- Botmasters only
    - Use `!none` as `<name>` to *remove* the playing status.
 - `$inviteme <server name>`Generates an instant invite to `<server name>`'s default channel and sends it to you via private message assuming the bot has permission and is currently connected to that server name. Get the list of currently connected servers using `|servers`.
    - Botmasters only
 - `$leave` Makes the bot leave the server the command was sent in.
    - Botmasters only
 
 ***Imgur Commands:*** *(Extension: imgur) (Must have configured `extensions/imgur/config.txt` with an Imgur API App ID/Secret for these to work!)*
 
 - `|imgur reddit <subreddit>` Gives a random image from the subreddit chosen. Example: `|imgur reddit funny`.
 - `|imgur search <query>` Searches imgur with the `query` and displays a random matching image.
 - `|imgur random` Displays an image from imgur's built-in random search.
 - `|imgur top [new]` Shows one of the top images from the gallery. If `new` is included (`|imgur top new`) it will sort the images by newest first.
 - `|imgur hot [new]` Shows one of the hottest images from the gallery. New works the same as with `|imgur top`.
 