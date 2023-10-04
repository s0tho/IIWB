from iiwb.client.iiwb import Reverse, __title__, __version__, __codename__, __fullcodename__
from discord.ext import commands
from discord.utils import get
import discord
from discord import app_commands
from discord import __version__ as dversion
import asyncio
import sys
import signal
import time

class Bot(Reverse):
	"""Bot class for IIWB"""
	
	def __new__(cls, command_prefix, description=None, **kwargs):
		"""__new__

		Parameters
		----------
		command_prefix : str
			Prefix used by the bot
		description : str, optional
			description, by default None

		Returns
		-------
		None
		"""
		return super(Bot, cls).__new__(cls)

	def __init__(self, command_prefix, description=None, **kwargs):
		"""__int__
		"""
		super().__init__(command_prefix, description, **kwargs)
		sys.tracebacklimit = 1
		self.prefix = command_prefix
		self.description = description
		self.initKwargs = kwargs
		self.registerEvents()
		self.isShutingdown = False

	def registerEvents(self):
		"""Register events
		"""
		self.getClient().event(self.on_ready)
		self.getClient().event(self.on_message)

	async def on_ready(self, ctx=None):
		"""on_ready

		Parameters
		----------
		ctx : context, optional
		"""		
		self.instance.tree.copy_global_to(guild= discord.Object(id=1101948059270791318))
		await self.instance.tree.sync(guild= discord.Object(id=1101948059270791318))
		print(f'Using {__title__} ver.{__version__} aka {__codename__} - Discord.py ver.{dversion}')
		print(f'Protocol {__fullcodename__}')
	
	async def run(self, token: str, status: str = "starting"):
		"""Start bot

		Parameters
		----------
		token : str
			Discord Token
		status : str, optional
			_description_, by default "starting"
		"""
		await super().run(token=token)
		print("{} successfully".format(status))

	def handler(signum, frame):
		"""Listener

		Parameters
		----------
		signum : str
		frame : str
		"""
		res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
		if res == 'y':
			exit(1)

	signal.signal(signal.SIGINT, handler)
	
	async def isShutingdown(self):
		"""Check if bot is shutting down"""
		return self.isShutingdown
				
		
