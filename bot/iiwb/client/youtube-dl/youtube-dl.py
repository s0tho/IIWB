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
    'source_address': '0.0.0.0', 
	# bind to ipv4 since ipv6 addresses cause issues sometimes
    'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
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
		self.playlist = []
		self.player = None
		

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
		name="streamyt",
		description="Start stream of youtube link.",
	)
	async def stream(self, ctx, url):
		"""Streams from a url (same as yt, but doesn't predownload)"""
		try:
			player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
			self.player = player
			ctx.voice_client.play(player, after=lambda e: self.pstream(ctx, "e"))
			await ctx.send('Now playing: {}'.format(player.title))
		except Exception as e:
			print(e)
			if(str(e) == "Already playing audio."):
				print("ADD TO PLAYLIST")
				player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
				await ctx.send(f"Adding to playlist : {player.title}")
				self.playlist.append(url)

	def pstream(self, ctx, url):
		try:
			if(self.voicechannel.is_playing()):
				print("already playing")
				return
			if(len(self.playlist) <= 0):
				asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."), self.bot.loop)
				return
			_url = self.playlist[0]
			asyncio.run_coroutine_threadsafe(self.stream(ctx, _url), self.bot.loop)
			del self.playlist[0]
		except Exception as e:
			print(e)

	@commands.hybrid_command(
		name="playlistyt",
		description="Send playlist of YTDL bot.",
	)
	async def playlistytdl(self, ctx):
		try:
			_li = "Playlist (I.I.W.B.) : \n"
			for i, row in enumerate(self.playlist, 0):
				player = await YTDLSource.from_url(row, loop=self.bot.loop, stream=True)
				_li += f"**N°{i}** {player.title}\n"
			await ctx.send(_li)
		except Exception as e:
			print(e)

	@commands.hybrid_command(
		name="resumeyt",
		description="Resume stream."
	)
	async def ytdlresume(self, ctx):
		if(len(self.playlist) >= 1):
			player = await YTDLSource.from_url(self.playlist[0], loop=self.bot.loop, stream=True)
			self.player = player
			ctx.voice_client.play(player, after=lambda e: self.pstream(ctx, "e"))
			await ctx.send('Now playing: {}'.format(player.title))
		else:
			print("Playlist empty")
	
	@commands.hybrid_command(
		name="stopyt",
		description="Stop current played video."
	)
	async def ytdlstop(self, ctx):
		await ctx.voice_client.disconnect()

	@commands.hybrid_command(
		name="clearyt",
		description="Stop current played video."
	)
	async def ytdlclear(self, ctx):
		await ctx.voice_client.disconnect()
		self.playlist = []

async def setup(bot):
	await bot.add_cog(youtubeDL(bot))