from iiwb.client.iiwb import Reverse, __title__, __version__, __codename__, __fullcodename__
from discord.ext import commands
from discord.utils import get
import discord
from discord import app_commands
from discord import __version__ as dversion
import asyncio
import sys

class Bot(Reverse):
	
	def __new__(cls, command_prefix, description=None, **kwargs):
		return super(Bot, cls).__new__(cls)

	def __init__(self, command_prefix, description=None, **kwargs):
		super().__init__(command_prefix, description, **kwargs)
		sys.tracebacklimit = 1
		self.prefix = command_prefix
		self.description = description
		self.initKwargs = kwargs
		self.registerEvents()
		self.isShutingdown = False

	def registerEvents(self):
		self.getClient().event(self.on_ready)
		self.getClient().event(self.on_message)

	async def on_ready(self, ctx=None):
		await self.tree.sync()
		print(f'Using {__title__} ver.{__version__} aka {__codename__} - Discord.py ver.{dversion}')
		print(f'Protocol {__fullcodename__}')
	
	async def run(self, token: str, status: str = "starting"):
		await super().run(token=token)
		print("{} successfully".format(status))
	
	async def isShutingdown(self):
		return self.isShutingdown
				
		
