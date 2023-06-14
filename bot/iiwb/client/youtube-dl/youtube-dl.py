import random
from discord.ext import commands
import discord
from iiwb.core import IIWBapi
import time
import asyncio
import yt_dlp as youtube_dl

__version__ = '0.5.0'

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    

class youtubeDL(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.voice = None
		self.room = []
		self.voicechannel = None
		self._basechannel = None
		

	@commands.hybrid_command(
		name="joinvc",
		description="The bot join your voice chat.",
	)
	async def rjoin(self, ctx):
		"""The bot will join the user voice channel

		Parameters
		----------
		ctx : Context
			
		"""
		try:
			author = ctx.message.author
			channel = author.voice.channel
			if(channel is None):
				await ctx.send("You are not connected to any voice channel.")
				pass
			self.voicechannel = await channel.connect()
			self.voice = self.voicechannel
			if(self.voicechannel):
				self._basechannel = channel
				self.room.append(ctx.channel.id)
				await ctx.send("The bot joined your voicechannel.")
		except Exception as e:
			print(e)


	@commands.hybrid_command(
		name="quitvc",
		description="The bot leave the voice chat.",
	)
	async def rquit(self, ctx):
		"""The bot will quit the voice channel he is in

		Parameters
		----------
		ctx : Context
		
		"""
		if(self.voicechannel):
			await self.voicechannel.disconnect()
			self.room = []
			await ctx.send("The bot left your voicechannel.")
		
	
	@commands.hybrid_command(
		name="stream",
		description="Start stream of youtube link.",
	)
	async def stream(self, ctx, url):
		"""Streams from a url (same as yt, but doesn't predownload)"""
		try:
			player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
			await ctx.send('Now playing: {}'.format(player.title))
		except Exception as e:
			print(e)
			if(str(e) == "Already playing audio."):
				print("ADD TO PLAYLIST")
			

async def setup(bot):
	await bot.add_cog(youtubeDL(bot))