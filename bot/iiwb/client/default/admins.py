import time
from discord.ext import commands
from discord import utils as ut
import discord
import asyncio
from iiwb.core import utils, IIWBapi


class Admins(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.b = IIWBapi()

	@commands.hybrid_command(
		name="clear",
		description="Delete x messages.",
	)
	async def clear(self, ctx, amount: int, wait: int = 0):
		""" Clear chat command """
		channel = ctx.message.channel
		author  = ctx.author
		guild   = ctx.guild

		if(await utils.specifiedRole("Cleaner", guild, author, ctx=ctx)):
			if(wait > 0):
				await ctx.send("Removed in {}".format(wait))
				await asyncio.sleep(wait)
			async for message in channel.history(limit=amount):
				try:
					newEntry = {
							"author": message.author.id,
							"authorname": message.author.name,
							"channel": message.channel.id,
							"guild": message.guild.id,
							"type": str(message.type),
							"message": message.content,
							"messageid": message.id,
							"created": time.mktime(message.created_at.timetuple()),
							"edited": message.edited_at,
							"deleted": time.time(),
							"deletor": ctx.author.id,
							"deletorname": ctx.author.name
						}
					pop = await self.b.insertClearRecord(newEntry)
				except Exception as e:
					print(e)
				await message.delete()
			await ctx.send(f"Vous avez supprimé {amount} messages.", ephemeral=True)
	

	@commands.hybrid_command(
		name="clearl",
		description="Delete x messages.",
	)
	async def clearl(self, ctx, channel: str, user: str, limit: int = 10):
		_channelid = channel[2:-1]
		_found = ut.get(ctx.guild.channels, id=int(_channelid))
		_userid = int(user[2:-1])

		print(f"We found your channel: {_found} {_found.id}")
		member = await ctx.guild.fetch_member(int(_userid))

		if(await utils.specifiedRole("Cleaner", ctx.guild, ctx.author, ctx=ctx)):
			_count = 0
			async for message in _found.history(limit=int(limit)):
				if message.author.id == _userid:
					_count += 1
					try:
						print(message)
						newEntry = {
									"author": message.author.id,
									"authorname": message.author.name,
									"channel": message.channel.id,
									"guild": message.guild.id,
									"type": str(message.type),
									"message": message.content,
									"messageid": message.id,
									"created": time.mktime(message.created_at.timetuple()),
									"edited": message.edited_at,
									"deleted": time.time(),
									"deletor": ctx.author.id,
									"deletorname": ctx.author.name
								}
						pop = await self.b.insertClearRecord(newEntry)
					except Exception as e:
						print(e)
					await message.delete()
					
			await ctx.send(f"Vous avez supprimé {_count} messages. contre: {member}, limit: {limit}", ephemeral=True)

	@commands.hybrid_command(
		name="bulkclear",
		description="Delete x messages.",
	)
	async def clearbulk(self, ctx, user: str, limit: int = 10):
		_userid = int(user[2:-1])
		member = await ctx.guild.fetch_member(int(_userid))
		_returnstr = []
		_count = 0
		if(await utils.specifiedRole("Cleaner", guild, author, ctx=ctx)):
			for channel in ctx.guild.channels:
				if(isinstance(channel, discord.TextChannel)):
					async for message in channel.history(limit=int(limit)):
						if message.author.id == _userid:
							try:
								newEntry = {
											"author": message.author.id,
											"authorname": message.author.name,
											"channel": message.channel.id,
											"guild": message.guild.id,
											"type": str(message.type),
											"message": message.content,
											"messageid": message.id,
											"created": time.mktime(message.created_at.timetuple()),
											"edited": message.edited_at,
											"deleted": time.time(),
											"deletor": ctx.author.id,
											"deletorname": ctx.author.name
										}
								pop = await self.b.insertClearRecord(newEntry)
							except Exception as e:
								print(e)
							_count +=1
							await message.delete()
							_returnstr += f"\nMessage supprimé dans {channel}, contre {member}, limit: {limit}"
			
			await ctx.send(_returnstr, ephemeral=True)

async def setup(bot):
	await bot.add_cog(Admins(bot))