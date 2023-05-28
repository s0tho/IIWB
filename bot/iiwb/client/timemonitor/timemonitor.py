from discord.ext import commands
import time
import asyncio

class TimeMonitor(commands.Cog):
    
	def __init__(self, bot):
		self.bot = bot
		self.tempStorage = {}
		self.storage = {}


	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if before.channel is None and after.channel is not None:
			#Rejoins une channel vocal
			print(f'{member.name} joined {after.channel.name}')

			# Start tracking the user's talk time
			start_time = time.time()

			self.tempStorage[member.id] = {after.channel.id: start_time}

			# Store this time
			print(self.tempStorage)
			print(self.storage)
		if before.channel is not None and after.channel is None:
			#Quitte le channel existant
			talk_time = round(time.time() - self.tempStorage[member.id][before.channel.id])

			if member.id not in self.storage:
				self.storage[member.id] = {before.channel.id: talk_time}
			else:
				if before.channel.id in self.storage[member.id]:
					self.storage[member.id][before.channel.id] += talk_time
				else:
					self.storage[member.id][before.channel.id] = talk_time

			#Remove temporary entry
			self.tempStorage.pop(member.id)

			print(f'{member.name} talk time: {talk_time} seconds')
			print(self.tempStorage)
			print(self.storage)
		if before.channel is not None and after.channel is not None:
			#Changement de channel
			print(f"{member.name} changed channel from {before.channel.name} to {after.channel.name}")

			start_time = time.time()
			talk_time = round(time.time() - self.tempStorage[member.id][before.channel.id])

			if member.id in self.tempStorage:
				self.tempStorage[member.id] = {after.channel.id: start_time}
			else:
				self.tempStorage[member.id][after.channel.id] = start_time

			print(self.tempStorage)

			if member.id not in self.storage:
				self.storage[member.id] = {before.channel.id: talk_time}
			else:
				if before.channel.id in self.storage[member.id]:
					self.storage[member.id][before.channel.id] += talk_time
				else:
					self.storage[member.id][before.channel.id] = talk_time

			#Remove temporary entry
			print(self.storage)
			
			

	
	@commands.command()
	async def getallrecord(self, ctx):
		await ctx.send("TEMPORARY : "+str(self.tempStorage))
		await ctx.send("STORAGE : "+str(self.storage))
		
async def setup(bot):
	await bot.add_cog(TimeMonitor(bot))