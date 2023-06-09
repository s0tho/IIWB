import time
from discord.ext import commands
from discord import utils as ut
import discord
import asyncio
import random
import time
from iiwb.core import utils, IIWBapi


class messageLogger(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.b = IIWBapi()
		self._expstore = {}
		self._temp = []

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
		
		await self.b.insertMessageLogger(_res)
		await self.insertexpstore(_res, message)


	async def insertexpstore(self, _json, message):
		try:
			data = [{
						"number_msg": 0,
						"last_exp": 0,
						"nen": 0,
						"userid": str(_json['author'])
					}]

			rave = await self.b.insertExperienceStore(data[0], str(_json['author']))
			""" self._expstore[_userid] = rave """
			self._expstore[str(_json['author'])] = rave
			print(self._expstore[str(_json['author'])])
			self._expstore[str(_json['author'])][0]['number_msg'] += 1

			if((self._expstore[str(_json['author'])][0]['number_msg'] - self._expstore[str(_json['author'])][0]['last_exp']) >= 5):
				print("5 or more")
				self._expstore[str(_json['author'])][0]['last_exp'] = self._expstore[str(_json['author'])][0]['number_msg']
				self._expstore[str(_json['author'])][0]['nen'] += random.randint(15, 25)

			await self.b.updateExperienceStore(self._expstore[str(_json['author'])][0], self._expstore[str(_json['author'])][0]['_id'])


		except Exception as e:
			print(e)
		

async def setup(bot):
	await bot.add_cog(messageLogger(bot))