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
from datetime import datetime
import ephem
from typing import List, Tuple

class MoonPhase(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cogs = utils.listCogs().keys()
		self.defaultCogs = ['reverse.client.default', 'reverse.client.debugger.debugger']

	def create_moon_art(self, phase):
		# Define moon symbols for each phase
		symbols = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌑']
		
		# Calculate the index of the moon symbol for the given phase
		index = int(round(phase / 100.0 * 8.0))
		
		# return the moon symbol
		return symbols[index]


	def get_phase_today(self):
		"""Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
		#Ephem stores its date numbers as floating points, which the following uses
		#to conveniently extract the percent time between one new moon and the next
		#This corresponds (somewhat roughly) to the phase of the moon.

		#Use Year, Month, Day as arguments
		date = ephem.Date(datetime.now())

		nnm = ephem.next_new_moon(date)
		pnm = ephem.previous_new_moon(date)

		lunation = (date-pnm)/(nnm-pnm)

		#Note that there is a ephem.Moon().phase() command, but this returns the
		#percentage of the moon which is illuminated. This is not really what we want.

		return lunation
	

	def current_moon_phase_name(self, phase):
		symbols = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full Moon', 'Waning Gibbous', 'Third Quarter', 'Waning Crescent', 'New Moon']
		
		index = int(round(phase / 100.0 * 8.0))

		return symbols[index]
	

	def today_print(self):
		aujourdhui = datetime.now()

		return f"Date et heure actuelles: {aujourdhui.strftime('%d %b %Y %Hh%M')}"



	@commands.hybrid_command(
		name="moon_phase",
		description="Return the current moon phase",

	)
	async def ping(self, ctx) -> None:
		current = self.get_phase_today() * 100
		moon = self.create_moon_art(current)
		name = self.current_moon_phase_name(current)
		embed = discord.Embed(title = "Moon phase", description = f"{self.today_print()}", color = 0x0060df)
		embed.add_field(name=f"{moon}", value=f"{current}%", inline=True)
		embed.add_field(name=f"", value=f"La lune est dans sa phase\n **{name}**", inline=True)
		await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(MoonPhase(bot))
