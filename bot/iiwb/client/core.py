import discord
from discord.ext import commands
from discord.utils import get
from iiwb.core._models import Context
from iiwb.core import utils
import asyncio
import sys
import json

class Core(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot: commands.Bot = bot
		self.cogs = utils.listCogs().keys()
		self.defaultCogs = ['reverse.client.default', 'reverse.client.debugger.debugger']

	@commands.hybrid_command(
		name="hey",
		description="Say hello to the bot",
		with_app_command=True
	)
	async def hey(self, ctx: commands.Context):
		await ctx.send("Hello! :wave:")

	@commands.hybrid_command(
		name="reload",
		description="Reload the bot",
		with_app_command=True
	)
	async def reload(self, ctx: commands.Context):
		ctx = Context(ctx)
		_kwargs, _args = utils.parse_args(args)
		data = {}
		self.cogs = utils.listCogs().keys()
		
		if("time" in _kwargs):
			time = int(_kwargs['time'])
		else:
			time = 0
		
		
		for cog in self.cogs:
			data[cog] = 'on'
		with open('cogs.json', 'w') as outfile:
			json.dump({**data, **_kwargs}, outfile)
		
		if(time > 0):
			await ctx.send(embed=utils.formatEmbed("Reload in {} seconds".format(time), ctx.author.name, **{**data, **_kwargs}))
			await asyncio.sleep(time)
		self.isShutingdown = True
		sys.tracebacklimit = 0
		raise SystemExit('Restarting The-Reverse')

	@commands.hybrid_command(
		name="where",
		description="Where is the bot",
		with_app_command=True
	)
	async def where(self, ctx: commands.Context):
		print(self.bot.guilds)
		await ctx.send("I'm on {} servers".format(len(self.bot.guilds)))

	@commands.hybrid_command(
		name="remindme",
		description="Remind you of something",
		with_app_command=True
	)
	async def remindme(self, ctx: commands.Context, time: int, message: str):
		await ctx.send("I will now wait {} seconds.".format(time))
		await asyncio.sleep(time)
		await ctx.send("Hey I didn't forget you! ;)\n Here your message : {}".format(message), ephemeral=True)

async def setup(bot):
	await bot.add_cog(Core(bot))