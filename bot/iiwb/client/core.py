from discord.ext import commands
from discord.utils import get
from iiwb.core._models import Context
from iiwb.core import utils
import asyncio
import sys
import json

__version__ = '0.9.0'

class Core(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cogs = utils.listCogs().keys()
		self.defaultCogs = ['reverse.client.default', 'reverse.client.debugger.debugger']

	@commands.command()
	async def hey(self, ctx):
		await ctx.send("Hello!")

	@commands.command()
	async def reload(self, ctx, *args):
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

	@commands.command()
	async def where(self,ctx):
		print(self.bot.guilds)

	@commands.command()
	async def remindme(self, ctx: Context, time: int, message: str):
		await ctx.send("I will now wait {} seconds.".format(time))
		await asyncio.sleep(time)
		await ctx.send("Hey I didn't forget you! ;)\n Here your message : {}".format(message))

async def setup(bot):
	await bot.add_cog(Core(bot))
