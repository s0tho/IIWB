import asyncio
from discord.ext import commands
import discord
from discord import app_commands
from iiwb.core._models import Server, Message, Context
from iiwb.core import utils, ReverseLogger
import random
from discord.utils import get

__title__ = 'IIWB'
__author__ = 'Hveodrungr'
__copyright__ = 'Copyright 2015-2023 Sacrezar'
__codename__ = 'I.I.W.B.'
__fullcodename__ = 'If I Were a (discord) Bot'
__version__ = '0.0.1'

class Reverse():

	def __init__(self, command_prefix, description=None, **kwargs):
		print('Reverse : {}'.format(kwargs))
		intents = discord.Intents.all()
		client = discord.Client(intents=intents)
		self.tree = app_commands.CommandTree(client)
		self.client = Server(commands.Bot(command_prefix=command_prefix, description=description, kwargs=kwargs, intents=intents))
		self.instance = self.getClient()
		self.cogs = []
		self.defaultCogs = ['reverse.client.core', 'reverse.client.default', 'reverse.client.debugger.debugger']
		self.toLoadCogs = utils.listCogs().keys()

		self.reverseNotepadLogger = ReverseLogger("ReverseNotepad", initLog=False)
		self.reverseNSALogger = ReverseLogger("ReverseNSA", consoleStream=True)
		self.reverseCountLogger = ReverseLogger("ReverseCount", initLog=False)

	async def run(self, token: str, cogs: list=[]):
		if(token is None):
			raise ValueError('Token can\t be empty.')
		if(not isinstance(token, str)):
			raise TypeError('Token is a string')
		self.token = token

		if(self.toLoadCogs):
			await self.linkCogs(self.toLoadCogs)
		else:
			await self.linkCogs(self.defaultCogs)
		
		self.running = await self.getClient().start(self.token)
		
	def getClient(self) -> commands.Bot:
		return self.client.getInstance()

	async def linkCogs(self, cogs: list):
		if(cogs is not None):
			self.cogs.extend(cogs)
		for cog in self.cogs:
			try:
				await self.getClient().load_extension(cog)
				print('Load {}'.format(cog))
			except Exception as e:
				print('{} cannot be loaded. [{}]'.format(cogs, e))
				self.getLogger()

	def getLogger(self):
		pass

	def getCommands(self) -> commands:
		return commands

	def createCommand(self, func, **kwargs) -> commands.Command:
		return commands.Command(func=func, kwargs=kwargs)

	def addCommand(self, _func, **kwargs) -> commands.command:
		command = commands.Command(func=_func, kwargs=kwargs)
		self.getClient().add_command(command)
		return command

	async def on_ready(self):
		self.client.sync(guild=discord.Object(id=1101948059270791318))
		print('We have logged in as {0.user}'.format(self.getClient()))
		
	async def on_message(self, message):
		m = Message(message)
		_attach = ""
		if(message.attachments):
			_attach+="\n"
			for i in utils.getObjectsAttr(message.attachments, "url"):
				_attach += "      -> {}\n".format(i)

		self.reverseNSALogger.info("[{0.channel}] <{0.guild}:{0.author}>: {0.content} {1}".format(m.getData(), _attach[:-1]))
		if(self.instance.user.mentioned_in(message)):
			self.reverseNotepadLogger.info("[{0.channel}] <{0.guild}:{0.author}>: {0.content} {1}".format(m.getData(), _attach[:-1]))

		ctx = Context(await self.getClient().get_context(message), __name__)

		await self.getClient().invoke(ctx)

	
	async def on_disconnect(self):
		print("Restart")
