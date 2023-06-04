from discord.ext import commands
import asyncio
from iiwb.core import utils


class NSALogger(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

		

async def setup(bot):
	await bot.add_cog(NSALogger(bot))