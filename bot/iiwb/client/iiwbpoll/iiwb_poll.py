from discord.ext import commands
import discord
from iiwb.core import utils, IIWBapi
import time
import asyncio


class PollButton(discord.ui.Button):

	def __init__(self, id, label, style):
		super().__init__(label=label, style=style)
		self.value = id
		self.label = label
		self.style = style
		self.b = IIWBapi()

	async def callback(self, interaction: discord.Interaction):
		# 
		try:
			if(not str(interaction.user.id) in IIWBPoll.POP[str(interaction.message.id)]['answer'][self.value]):
				IIWBPoll.POP[str(interaction.message.id)]['answer'][self.value].append(f'{interaction.user.id}')
				IIWBPoll.POP[str(interaction.message.id)]['total'] += 1
				

			# Create Embed to stock values
			embed = discord.Embed(title = "Poll", description = f"{IIWBPoll.POP[str(interaction.message.id)]['question']}", color = 0x0060df)

			_vote = 0
			try:

				print(IIWBPoll.POP[str(interaction.message.id)])

				for row in IIWBPoll.POP[str(interaction.message.id)]['answer']:
					print(row)
					print(IIWBPoll.POP[str(interaction.message.id)]['answer'][row])
					print(f"STOP"+str(str(interaction.message.id)) in IIWBPoll.POP[str(interaction.message.id)]['answer'][row])
					if(str(str(interaction.message.id)) in IIWBPoll.POP[str(interaction.message.id)]['answer'][row]):
						_vote += 1 
						if(_vote > IIWBPoll.POP[str(interaction.message.id)]['maxVote']):
							await interaction.response.send_message('You already voted!', ephemeral=True)
							return
							
						if(_vote < IIWBPoll.POP[str(interaction.message.id)]['maxVote']):
							print("Still more vote to go")
							
			except Exception as e:
				print(e)
				
			# Create field for answer
			try:
				for id, row in enumerate(IIWBPoll.POP[str(interaction.message.id)]['ordered'],  1):
					
					print("poollbutton ", id, row)
					_maths = (len(IIWBPoll.POP[str(interaction.message.id)]['answer'][row]) / IIWBPoll.POP[str(interaction.message.id)]['total'])*100
					print(_maths)
					
					embed.add_field(name=f"N°{id} {row} - {round(_maths, 2)}%", value="", inline=False)
			except Exception as e:
				print(e)
				
			embed.add_field(name=f"Vote total : {IIWBPoll.POP[str(interaction.message.id)]['total']}", value="", inline=False)

			_tempjson = {f'{str(interaction.message.id)}':{
				"_id": interaction.message.id,
				"question": IIWBPoll.POP[str(interaction.message.id)]['question'],
				"created": IIWBPoll.POP[str(interaction.message.id)]['created'],
				"finished": IIWBPoll.POP[str(interaction.message.id)]['finished'],
				"duration": IIWBPoll.POP[str(interaction.message.id)]['duration'],
				"answer": IIWBPoll.POP[str(interaction.message.id)]['answer'],
				"ordered": IIWBPoll.POP[str(interaction.message.id)]['ordered'],
				"maxVote":  IIWBPoll.POP[str(interaction.message.id)]['maxVote'],
				"total": IIWBPoll.POP[str(interaction.message.id)]['total'],
				"_uid": IIWBPoll.POP[str(interaction.message.id)]['_uid'],
				"_rev": IIWBPoll.POP[str(interaction.message.id)]['_rev']
			}}
			
			print(IIWBPoll.POP[str(interaction.message.id)]['_uid'])
			print(_tempjson)
			a = await self.b.updatePoll(IIWBPoll.POP[str(interaction.message.id)]['_uid'], _tempjson)
			print('Update - answer')
			print(a)

			await interaction.response.edit_message(embed=embed)
			#print(IIWBPoll.STORAGE)
			print(interaction.message.id in IIWBPoll.STORAGE)
		except Exception as e:
			print(e)

class ResetButton(discord.ui.Button):
	
	def __init__(self, id, label, style):
		super().__init__(label=label, style=style)
		self.value = id
		self.label = label
		self.style = style
		self.b = IIWBapi()


	async def callback(self, interaction: discord.Interaction):
		storage = 0
		try:
			print('YAY')
			print(IIWBPoll.POP[str(interaction.message.id)])
			""" await interaction.response.send_message('TIME TO RESET ALL VALUES', ephemeral=True) """

			for row, value in IIWBPoll.POP[str(interaction.message.id)]['answer'].items():
				print("ITEM ENUMERATE ", row, value)
				if(str(interaction.user.id) in value):
					storage += 1
					_d = value.index(str(interaction.user.id) )
					print(_d)
					value.pop(_d)
					IIWBPoll.POP[str(interaction.message.id)]['total'] -= 1

				

				""" if(not str(interaction.user.id) in IIWBPoll.POP[str(interaction.message.id)]['answer'][self.label]):
					IIWBPoll.POP[str(interaction.message.id)]['answer'][self.label].append(f'{str(interaction.user.id)}')
					IIWBPoll.POP[str(interaction.message.id)]['total'] += 1  """
		except Exception as e:
			print(e)

		try:
			print('YAYA')
			# Create Embed to stock values
			embed = discord.Embed(title = "Poll", description = f"{IIWBPoll.POP[str(interaction.message.id)]['question']}", color = 0x0060df)
			print(IIWBPoll.POP)
			print('letsgo')
			
			# Create field for answer
			for id, row in enumerate(IIWBPoll.POP[str(interaction.message.id)]['ordered'],  1):
				#print(row)
				print("+1", id, row, IIWBPoll.POP[str(interaction.message.id)]['answer'][row])
				if(IIWBPoll.POP[str(interaction.message.id)]['total'] <= 0):
					_maths = (len(IIWBPoll.POP[str(interaction.message.id)]['answer'][row]) / 1)*100
				else:
					_maths = (len(IIWBPoll.POP[str(interaction.message.id)]['answer'][row]) / (IIWBPoll.POP[str(interaction.message.id)]['total']))*100
				embed.add_field(name=f"N°{id} {row} - {round(_maths, 2)}%", value="", inline=False)

				
			embed.add_field(name=f"Vote total : {IIWBPoll.POP[str(interaction.message.id)]['total']}", value="", inline=False)	

			_tempjson = {f'{str(interaction.message.id)}':{
				"_id": interaction.message.id,
				"question": IIWBPoll.POP[str(interaction.message.id)]['question'],
				"created": IIWBPoll.POP[str(interaction.message.id)]['created'],
				"finished": IIWBPoll.POP[str(interaction.message.id)]['finished'],
				"duration": IIWBPoll.POP[str(interaction.message.id)]['duration'],
				"answer": IIWBPoll.POP[str(interaction.message.id)]['answer'],
				"ordered": IIWBPoll.POP[str(interaction.message.id)]['ordered'],
				"maxVote":  IIWBPoll.POP[str(interaction.message.id)]['maxVote'],
				"total": IIWBPoll.POP[str(interaction.message.id)]['total'],
				"_uid": IIWBPoll.POP[str(interaction.message.id)]['_uid'],
				"_rev": IIWBPoll.POP[str(interaction.message.id)]['_rev']
			}}
			
			
			a = await self.b.updatePoll(IIWBPoll.POP[str(interaction.message.id)]['_uid'], _tempjson)
			print('Update - total')
			print(a)

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
		self.b = IIWBapi()


	@commands.hybrid_command(
		name="poller",
		description="Create a poll",
	)
	async def gfan(self, ctx, question, first, second, third='0', fourth='0', fifth='0', duration=10, maxvote=1):
		
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
		from collections import OrderedDict
		_itemtovote = OrderedDict()
		_itemset = []
		i=1
		for id, (key, value) in enumerate(args.items(), 1):
			print(key, value)
			if(value == None or value == 0 or value == '0'):
				print(f"Entry {key} empty - {value}")
			else:
				_itemtovote.update({str(value): []})
				_itemset.append(str(value))
				
				_args[key] = 0
				_items[key] = value
			i += 1
		
		try:
			for id, value in enumerate(_itemset, 1):
				view.add_item(PollButton(id=value, label=id, style=discord.ButtonStyle.blurple))
				embed.add_field(name=f"N°{id} {value} - 0%", value="", inline=False)

			view.add_item(ResetButton(id="Reset", label="Reset", style=discord.ButtonStyle.red))
		except Exception as e:
			print(e)
		
		_storage = await ctx.send(embed=embed, view=view)
		print("value")
		print(_itemtovote)
		print(_storage)
		print("value")
		print(_itemset)
		
		IIWBPoll.STORAGE[_storage.id] = {
			"message": _storage,
			"vote": {},
			"choice": _args,
			"item": _items,
			"total": 0
		}

		start_time = time.time()

		_tempjson = {f'{_storage.id}':{
			"_id": _storage.id,
			"question": question,
			"created": start_time,
			"finished": (start_time + (duration * 60)),
			"duration": duration,
			"answer": _itemtovote,
			"ordered": _itemset,
			"maxVote": maxvote,
			"total": 0
		}}


		a = await self.b.insertPoll(_tempjson)
		print(f'Incroyable{a}')
		a[f'{_storage.id}']['_uid'] = a['_id']
		a[f'{_storage.id}']['_rev'] = a['_rev']
		IIWBPoll.POP[str(_storage.id)] = a[str(_storage.id)]
		print("POP value")
		print(IIWBPoll.POP)

	

async def setup(bot):
	await bot.add_cog(IIWBPoll(bot))