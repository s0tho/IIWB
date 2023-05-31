from discord.ext import commands
import discord
from iiwb.core._service import IIWBGeopy, SqliteService, IIWBapi, Route
from iiwb.core import utils
from datetime import datetime
import ephem
import math
from typing import List, Tuple
from discord.ext import commands


class ViewMoonPhase(discord.ui.View):

	def __init__(self):
		super().__init__(timeout=None)
		self.value = None
		self.db = SqliteService('moonphase.db')


	@discord.ui.button(label='Send Message', style=discord.ButtonStyle.grey)
	async def yahallo_message(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message('Hello from the button!', ephemeral=True)


	@discord.ui.button(label='Update', style=discord.ButtonStyle.grey)
	async def edit_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
		city = await MoonPhase._getcitybyid(interaction.user.id)
		if city is None:
			city = 'Rouen'
		
		if (coor := IIWBGeopy.get_coordinates(city)) is not None:
			latitude, longitude = coor

		current = MoonPhase.get_phase_today() * 100
		moon = MoonPhase.create_moon_art(current)
		name = MoonPhase.current_moon_phase_name(current)
		boussole = MoonPhase.get_compass(latitude, longitude) 
		embed = discord.Embed(title = "Moon phase", description = f"{MoonPhase.today_print()} et vous êtes dans la ville de **{city}**", color = 0x0060df)
		embed.add_field(name=f"{moon}", value=f"{current}%", inline=True)
		embed.add_field(name=f"", value=f"La lune est dans sa phase\n **{name}** \n {boussole}", inline=True)
		await interaction.response.edit_message(embed=embed)


class MoonPhase(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cogs = utils.listCogs().keys()
		self.defaultCogs = ['reverse.client.default', 'reverse.client.debugger.debugger']
		self.db = SqliteService('moonphase.db')
		self.db.createTable('moon_phase', 'id integer PRIMARY KEY, city text')
		self.b = IIWBapi()
		""" self._env = utils.load_backend()
		try:
			self.config = utils.load_custom_config('config.json', __file__, path='')
		except:
			self.config = None """


	@staticmethod
	def create_moon_art(phase):
		# Define moon symbols for each phase
		symbols = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌑']
		
		# Calculate the index of the moon symbol for the given phase
		index = int(round(phase / 100.0 * 8.0))
		
		# return the moon symbol
		return symbols[index]


	@staticmethod
	def get_phase_today():
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
	

	@staticmethod
	def current_moon_phase_name(phase):
		symbols = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full Moon', 'Waning Gibbous', 'Third Quarter', 'Waning Crescent', 'New Moon']
		
		index = int(round(phase / 100.0 * 8.0))

		return symbols[index]
	

	@staticmethod
	def today_print():
		aujourdhui = datetime.now()

		return f"Date et heure actuelles: {aujourdhui.strftime('%d %b %Y %Hh%M')}"


	@staticmethod
	def get_compass(latitude, longitude):
		# Création de l'objet d'observateur pour les coordonnées données
		observer = ephem.Observer()
		observer.lat = latitude
		observer.lon = longitude

		# Création de l'objet Lune
		moon = ephem.Moon(observer)

		# Calcul de l'azimut et de l'élévation de la Lune
		moon_azimuth = moon.az * 180 / math.pi  # conversion en degrés
		moon_elevation = moon.alt * 180 / math.pi  # conversion en degrés

		# Calcul de la boussole de la Lune (en utilisant l'azimut de la Lune et le nord magnétique)
		north_mag = 0  # azimut du nord magnétique (en degrés)
		moon_compass = (moon_azimuth - north_mag + 360) % 360  # boussole de la Lune (en degrés)

		# Affichage du résultat
		return f"Boussole de la Lune :**{moon_compass}** :arrow_upper_right: degrés  "


	@staticmethod
	def getcitybyid(instance, id):
		_uid = id
		row = instance.selectbyid('moon_phase', 'id', _uid)
		
		if len(row) >= 1:
			row = row[0]
			uid, city = row
			return city
		else:
			return None
	
	@staticmethod
	async def _getcitybyid(id):
		_uid = id
		b = IIWBapi()
		b = await b.getuserbyid(_uid)
		if(b['_id'] is not None):
			return b['city']
		else:
			return None
		

	@commands.hybrid_command(
		name="moon_phase",
		description="Return the current moon phase",

	)
	async def moon_phase(self, ctx) -> None:
		current = MoonPhase.get_phase_today() * 100
		city = await MoonPhase._getcitybyid(ctx.author.id)
		
		if city is None:
			city = 'Rouen'
		
		if (coor := IIWBGeopy.get_coordinates(city)) is not None:
			latitude, longitude = coor

		moon = MoonPhase.create_moon_art(current)
		name = MoonPhase.current_moon_phase_name(current)
		boussole = MoonPhase.get_compass(latitude, longitude)
		embed = discord.Embed(title = "Moon phase", description = f"{MoonPhase.today_print()} et vous êtes dans la ville de **{city}**", color = 0x0060df)
		embed.add_field(name=f"{moon}", value=f"{current}%", inline=True)
		embed.add_field(name=f"", value=f"La lune est dans sa phase\n **{name}** \n {boussole}", inline=True)
		
		view = ViewMoonPhase()
		await ctx.send(embed=embed, view=view)


	@commands.hybrid_command(
		name="geocity",
		description="Returns the longitude and latitude of the specified city",

	)
	async def geocity(self,ctx, city):
		if (coor := IIWBGeopy.get_coordinates(city)) is not None:
			latitude, longitude = coor
			await ctx.send(f"La latitude et la longitude de la ville de {city} sont :{latitude}, {longitude}")

			j = {
				"_id": str(ctx.author.id),
				"city": f"{city}"
			}
			await self.b.addusermp(j)
			await self.b.updateuser(ctx.author.id, j)
		else:
			await ctx.send(f"Coordonnées non trouvées pour {city}. Veuillez vérifier le nom de la ville.")


	@commands.hybrid_command(
		name="wherami",
		description="Returns the city in which you are registered",

	)
	async def gfan(self, ctx):
		city = await MoonPhase._getcitybyid(ctx.author.id)
		
		if city:
			await ctx.send(f"Vous êtes inscrit sur la ville de {city}.")
		else:
			await ctx.send("Vous n'êtes inscrit nulle part, par défaut à Rouen.")


	@commands.command()
	async def testapi(self, ctx):
		j = {
			"_id": str(ctx.author.id),
			"city": "Rouen"
		}
		b = await self.b.addusermp(j)
		await ctx.send(b)

	@commands.command()
	async def testuser(self, ctx):
		b = await self.b.getuserbyid(ctx.author.id)
		if(b['_id'] is not None):
			await ctx.send(b['city'])
		else:
			await ctx.send('No document using this id.')
	
	@commands.command()
	async def testcity(self, ctx, city):
		j = {
			"_id": str(ctx.author.id),
			"city": f"{city}"
		}
		b = await self.b.updateuser(ctx.author.id, j)
		print(b)

	#Example embedded message and update using button
	""" @commands.command()
	async def yahallo(self, ctx):
		print("call")
		embed = discord.Embed(title='Hello!', description='Click the button to send a message.')
		view = ViewMoonPhase()
		await ctx.reply(embed=embed, view=view) """


async def setup(bot):
	await bot.add_cog(MoonPhase(bot))
