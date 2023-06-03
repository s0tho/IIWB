from discord.ext import commands
import discord
from iiwb.core import utils
import time
import asyncio


class PollButton(discord.ui.Button):

	def __init__(self, id, label, style):
		super().__init__(label=label, style=style)
		self.value = id
		self.label = label
		self.style = style

	async def callback(self, interaction: discord.Interaction):
		# 
		if(not str(interaction.user.id) in IIWBPoll.POP[interaction.message.id]['answer'][self.value]):
			IIWBPoll.POP[interaction.message.id]['answer'][self.value].append(f'{interaction.user.id}')
			IIWBPoll.POP[interaction.message.id]['total'] += 1
			

		# Create Embed to stock values
		embed = discord.Embed(title = "Poll", description = f"{IIWBPoll.POP[interaction.message.id]['question']}", color = 0x0060df)

		_vote = 0
		try:

			for row in IIWBPoll.POP[interaction.message.id]['answer']:
				print(row)
				print(IIWBPoll.POP[interaction.message.id]['answer'][row])
				print(f"STOP"+str(interaction.user.id) in IIWBPoll.POP[interaction.message.id]['answer'][row])
				if(str(interaction.user.id) in IIWBPoll.POP[interaction.message.id]['answer'][row]):
					_vote += 1 
					if(_vote > IIWBPoll.POP[interaction.message.id]['maxVote']):
						await interaction.response.send_message('You already voted!', ephemeral=True)
						return
						
					if(_vote < IIWBPoll.POP[interaction.message.id]['maxVote']):
						print("Still more vote to go")
						
		except Exception as e:
			print(e)
			
		# Create field for answer
		for id, row in enumerate(IIWBPoll.POP[interaction.message.id]['answer'],  1):

			_maths = (len(IIWBPoll.POP[interaction.message.id]['answer'][row]) / IIWBPoll.POP[interaction.message.id]['total'])*100
			
			embed.add_field(name=f"N°{id} {row} - {round(_maths, 2)}%", value="", inline=False)

			
		embed.add_field(name=f"Vote total : {IIWBPoll.POP[interaction.message.id]['total']}", value="", inline=False)	

		await interaction.response.edit_message(embed=embed)
		#print(IIWBPoll.STORAGE)
		print(interaction.message.id in IIWBPoll.STORAGE)

class ResetButton(discord.ui.Button):
	
	def __init__(self, id, label, style):
		super().__init__(label=label, style=style)
		self.value = id
		self.label = label
		self.style = style


	async def callback(self, interaction: discord.Interaction):
		storage = 0
		for id, (row, value) in enumerate(IIWBPoll.POP[interaction.message.id]['answer'].items(),0):

			if(str(interaction.user.id) in value):
				storage += 1
				_d = value.index(str(interaction.user.id) )
				value.pop(_d)
				IIWBPoll.POP[interaction.message.id]['total'] -= 1

		try:

			if(not str(interaction.user.id) in IIWBPoll.POP[interaction.message.id]['answer'][self.label]):
				IIWBPoll.POP[interaction.message.id]['answer'][self.label].append(f'{interaction.user.id}')
				IIWBPoll.POP[interaction.message.id]['total'] += 1
		except Exception as e:
			print(e)

		try:
			# Create Embed to stock values
			embed = discord.Embed(title = "Poll", description = f"{IIWBPoll.POP[interaction.message.id]['question']}", color = 0x0060df)
			print(IIWBPoll.POP)
			# Create field for answer
			for id, row in enumerate(IIWBPoll.POP[interaction.message.id]['answer'],  1):
				print(row)
				_maths = (len(IIWBPoll.POP[interaction.message.id]['answer'][row]) / (IIWBPoll.POP[interaction.message.id]['total']+1))*100
				embed.add_field(name=f"N°{id} {row} - {round(_maths, 2)}%", value="", inline=False)

				
			embed.add_field(name=f"Vote total : {IIWBPoll.POP[interaction.message.id]['total']}", value="", inline=False)	

			await interaction.response.edit_message(embed=embed)
			#print(IIWBPoll.STORAGE)
			print(interaction.message.id in IIWBPoll.STORAGE)
		except Exception as e:
			print(e)
			

class IIWBPoll(commands.Cog):

	STORAGE = {}
	SACREZAR = {}
	POP = {}
	
	def __init__(self, bot):
		self.bot = bot
		self.tempStorage = {}
		self.storage = {}


	
	@commands.hybrid_command(
		name="poll",
		description="Returns the city in which you are registered",

	)
	async def gfan(self, ctx, question, first, second, third = '0', fourth = '0', fifth = '0', duration = 10, maxVote=1):
		
		args = {
			"first": first,
			"second": second,
			"third": third,
			"fourth": fourth,
			"fifth": fifth
		}

		view = discord.ui.View(timeout=None)

		embed = discord.Embed(title = "Poll", description = f"{question}", color = 0x0060df)
		_args = {}
		_items = {}
		_itemtovote = {}
		i=1
		for key, value in args.items():
			print(key, value)
			if(value == None or value == 0 or value == '0'):
				print(f"Entry {key} empty - {value}")
			else:
				_itemtovote.update({
					f"{value}": []
				})
				view.add_item(PollButton(id=value, label=key, style=discord.ButtonStyle.blurple))
				embed.add_field(name=f"N°{i} {value} - 0%", value="", inline=False)
				_args.update({
					f"{key}": 0
				})
				_items[key] = value
			i += 1
		
		view.add_item(ResetButton(id="Reset", label="Reset", style=discord.ButtonStyle.red))

		_storage = await ctx.send(embed=embed, view=view)
		print(_itemtovote)
		
		IIWBPoll.STORAGE[_storage.id] = {
			"message": _storage,
			"vote": {},
			"choice": _args,
			"item": _items,
			"total": 0
		}

		start_time = time.time()

		IIWBPoll.POP[_storage.id] = {
			"_id": _storage.id,
			"question": question,
			"created": start_time,
			"finished": (start_time + (duration * 60)),
			"answer": _itemtovote,
			"maxVote": maxVote,
			"total": 0
		}

		print(IIWBPoll.POP)


async def setup(bot):
	await bot.add_cog(IIWBPoll(bot))