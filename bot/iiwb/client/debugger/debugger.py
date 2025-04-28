from discord.ext import commands, tasks
import asyncio
from urllib import parse
from discord import Embed

from iiwb.core._models import Context, Role
from iiwb.core import utils

class Debugger(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		try:
			self.config = utils.load_custom_config('config.json', __file__, path='')
		except:
			self.config = None
	

	@commands.command()
	async def showModules(self, ctx):
		ctx = Context(ctx)
		embed=Embed(title="Loaded Modules", color=0xe80005)
		embed.set_author(name="The reverse")
		for key, value in utils.listCogs(filterIn={'on', 'off'}).items():
			embed.add_field(name=key, value=value, inline=False)
		embed.set_footer(text="Asked by {}".format(ctx.author.name))
		message = await ctx.send(embed=embed)
	

async def setup(bot):
	await bot.add_cog(Debugger(bot))