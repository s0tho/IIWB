from typing import Optional
from discord.ext import commands
import discord
from discord import app_commands
from discord.utils import get
from iiwb.core._models import Context
from iiwb.core import utils
import asyncio
import sys
import json

class MoonPhase(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cogs = utils.listCogs().keys()
		self.defaultCogs = ['reverse.client.default', 'reverse.client.debugger.debugger']

	@app_commands.command()
	async def ping(self, interaction: discord.Interaction) -> None:
		ping1 = f"{str(round(self.client.latency * 1000))} ms"
		embed = discord.Embed(title = "**Pong!**", description = "**" + ping1 + "**", color = 0xafdafc)
		await interaction.response.send_message(embed = embed)

	
	@commands.hybrid_command(name="first_slash")
	async def first_slash(self, ctx): 
		await ctx.send("You executed the slash command!") #respond no longer works, so i changed it to send


async def setup(bot):
	await bot.add_cog(MoonPhase(bot))
