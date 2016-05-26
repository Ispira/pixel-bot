#Music commands v0.0.2
from discord.ext import commands
from discord import opus

from checks import *

#Get opus ready
opus.load_opus("libopus-0.x64.dll")

class Music():
    def __init__(self, bot):
        self.bot = bot
        self.vclient = None
        self.vplayer = None
    
    ## Play a youtube video in the current channel
    @commands.command(pass_context=True)
    @allowed(0, '|')
    async def yt(self, ctx, url: str):
            mchannel = ctx.message.author.voice_channel
            if mchannel is None:
                await self.bot.say("You must be in a voice channel!")
                return
        
            if self.vclient is None:
                self.vclient = await self.bot.join_voice_channel(mchannel)
            elif self.vplayer.is_playing():
                self.vplayer.stop()
            try:
                self.vplayer = await self.vclient.create_ytdl_player(url)
                await self.bot.say("Playing video!")
                self.vplayer.start()
            except Exception as error:
                await self.bot.send_message(ctx.message.channel,"Error: {0}"
                .format(error))
    
    def __del__(self):
        if self.vplayer is not None:
            if self.vplayer.is_playing():
                self.vplayer.stop()
        self.vplayer = None
        
        if self.vclient is not None:
            self.vclient.disconnect()
            self.vclient = None

def setup(bot):
    bot.add_cog(Music(bot))