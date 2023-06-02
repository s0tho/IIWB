from discord.ext import commands
import asyncio
from iiwb.core import utils


class Admins(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

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
			async for message in channel.history(limit=amount+1):
				await message.delete()
			await ctx.send(f"Vous avez supprimé {amount} messages.", ephemeral=True)

async def setup(bot):
	await bot.add_cog(Admins(bot))