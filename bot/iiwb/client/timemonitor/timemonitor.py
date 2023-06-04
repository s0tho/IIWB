from discord.ext import commands
from iiwb.core import IIWBapi
import time
import asyncio

class TimeMonitor(commands.Cog):
    
	def __init__(self, bot):
		self.bot = bot
		self.tempStorage = {}
		self.storage = {}
		self.b = IIWBapi()


	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if before.channel is None and after.channel is not None:
			# Join voicechat
			print(f'{member.name} joined {after.channel.name}')

			# Start tracking the user's talk time
			start_time = time.time()
			
			# Create dict with user's entry
			j = {
				'userid': f"{member.id}",
				'status': {
					'channel': f"{after.channel.id}",
					'connected': start_time,
					'disconnected': 0,
					'duration': 0
				}
			}

			# Send and get modified entry
			j = await self.b.adduser_timemonitor(j)
			self.storage[j['userid']] = j
			self.tempStorage[member.id] = {after.channel.id: start_time}

		if before.channel is not None and after.channel is None:
			# Leave existing voicechat
			print(f"{member.name} is leaving voice chat.")
			
			# Get user's entry
			_bfore = self.storage[str(member.id)]
			# Calculate duration
			_bfore['status']['disconnected'] = time.time()
			_bfore['status']['duration'] = _bfore['status']['disconnected'] - _bfore['status']['connected']

			# Create input and send it
			input = {
				'userid': _bfore['userid'],
				'status': _bfore['status']
			}
			res = await self.b.updatetimemonitor(_bfore['_id'], input)

		if before.channel is not None and after.channel is not None:
			# Change voicechat
			print(f"{member.name} changed channel from {before.channel.name} to {after.channel.name}")

			# Store db entry for later
			_bfore = self.storage[str(member.id)]
			# Calculate duration of the time spend in VC
			_bfore['status']['disconnected'] = time.time()
			_bfore['status']['duration'] = _bfore['status']['disconnected'] - _bfore['status']['connected']

			# Create input with modified entries
			input = {
				'userid': _bfore['userid'],
				'status': _bfore['status']
			}

			# Update time monitor entry for user
			res = await self.b.updatetimemonitor(_bfore['_id'], input)


			# Create new user for the new channel
			# Start tracking the user's talk time
			start_time = time.time()
			
			j = {
				'userid': f"{member.id}",
				'status': {
					'channel': f"{after.channel.id}",
					'connected': start_time,
					'disconnected': 0,
					'duration': 0
				}
			}

			j = await self.b.adduser_timemonitor(j)

			self.storage[j['userid']] = j
		
		
async def setup(bot):
	await bot.add_cog(TimeMonitor(bot))