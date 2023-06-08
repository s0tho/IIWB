import time
from discord.ext import commands
from discord import utils as ut
import discord
import asyncio
import time
from iiwb.core import utils, IIWBapi


class messageLogger(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.b = IIWBapi()

	@commands.Cog.listener()
	async def on_message(self, message):
		_res = {
			"id": message.id,
			"channelid": message.channel.id,
			"author": message.author.id,
			"guildid": message.guild.id,
			"content": message.content,
			"created_at": time.mktime(message.created_at.timetuple()),
			"mention_everyone": message.mention_everyone,
			"pinned": message.pinned,
			"position": message.position,
			"attachments": message.attachments,
			"webhook_id": message.webhook_id
		}
		
		if(message.attachments != []):
			_attach = []
			for i in utils.getObjectsAttr(message.attachments, "url"):
				_attach.append(i)
			_res["attachments"] = _attach


		if(message.edited_at != None):
			_res["edited_at"] = time.mktime(message.edited_at.timetuple()),

		_rep = await self.b.insertMessageLogger(_res)
		print(_rep)



async def setup(bot):
	await bot.add_cog(messageLogger(bot))