from discord.ext import commands
import discord
from iiwb.core import utils
from PIL import Image, ImageDraw, ImageFont, ImageOps

class IIWBExperience(commands.Cog):

	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot

	
	@staticmethod
	def drawProgressBar(d, x, y, w, h, progress, bg="black", fg="red"):
		# draw background
		d.ellipse((x+w, y, x+h+w, y+h), fill=bg)
		d.ellipse((x, y, x+h, y+h), fill=bg)
		d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)

		# draw progress bar
		w *= progress
		d.ellipse((x+w, y, x+h+w, y+h),fill=fg)
		d.ellipse((x, y, x+h, y+h),fill=fg)
		d.rectangle((x+(h/2), y, x+w+(h/2), y+h),fill=fg)

		return d


	@commands.command()
	async def expdemo(self, ctx):
		try:
			# Set the dimensions of the image
			width, height = 600, 200
			lvl, xp, nextlvl = 10, 150, 1250

			# Create a transparent image with RGBA mode
			image = Image.new("RGB", (width, height), (35, 39, 42))

			# Specify the font size and font path (change it to your preferred font file)
			font_size = 40
			font_path = "C:\Windows\Fonts\corbell.ttf"

			# Load the font with the specified size
			font = ImageFont.truetype(font_path, font_size)

			# Create a drawing object
			draw = ImageDraw.Draw(image)

			# Set color
			white = (255, 255, 255)  # White color
			pink = (233, 101, 165)
			red = (255, 0, 0)

			t = [{
					"name": str(ctx.author.name),
					"x": 150,
					"y": 100,
					"color": red,
					"size": 40,
					"resize": False
				},{
					"name": f"RANK",
					"x": 400,
					"y": 30,
					"color": white,
					"size": 20,
					"resize": False

				},{
					"name": f"#1",
					"x": 400,
					"y": 15,
					"color": white,
					"size": 40,
					"resize": {
						'name': 'RANK',
						'size': 20
					}

				},{
					"name": f"LEVEL",
					"x": 500,
					"y": 30,
					"color": red,
					"size": 20,
					"resize": False
				},{
					"name": f"10",
					"x": 500,
					"y": 15,
					"color": red,
					"size": 40,
					"resize": {
						'name': 'LEVEL',
						'size': 20
					}
				},{
					"name": f"125 ",
					"x": 400,
					"y": 110,
					"color": white,
					"size": 30,
					"resize": False
				},{
					"name": f" / 850",
					"x": 400,
					"y": 110,
					"color": white,
					"size": 30,
					"resize": {
						'name': '125',
						'size': 30
					}
				}
				
			]
			
			""" # Calculate the text position at the center of the image
			text_width, text_height = draw.textsize(text, font=font)
			text_x = 150
			text_y = 100 """

			d = IIWBExperience.drawProgressBar(draw,180,150,350,25,round(xp/nextlvl, 2))

			# Draw the text on the image
			for row in t:
				font = ImageFont.truetype(font_path, row['size'])
				print(row)
				if(row['resize']):
					print("true")
					fontu = ImageFont.truetype(font_path, row['resize']['size'])
					row['x'] = row['x']+draw.textsize(row['resize']['name'], font=fontu)[0]
				draw.text((row['x'], row['y']), row['name'], fill=row['color'], font=font)
				
			# Create circular thumbnail
			im = Image.open('default.jpg')
			im = im.resize((120, 120));
			bigsize = (im.size[0] * 3, im.size[1] * 3)
			mask = Image.new('L', bigsize, 0)
			draw = ImageDraw.Draw(mask) 
			draw.ellipse((0, 0) + bigsize, fill=255)
			mask = mask.resize(im.size, Image.ANTIALIAS)
			im.putalpha(mask)

			output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
			output.putalpha(mask)
			output.save('output.png')
			# Add image to the rank image
			image.paste(im, (20, 50), im)
			
			# Get storage path
			import os
			cwfd = os.path.dirname(os.path.realpath(__file__))
			fn = "lets_goo.png"
			jsonf = os.path.realpath(os.path.join(cwfd, 'rank', fn))
			
			# Save the image as a PNG file
			image.save(jsonf)
			file = discord.File(jsonf, filename=fn)
			await ctx.send(file=file)
		except Exception as e:
			print(e)

		


async def setup(bot):
	await bot.add_cog(IIWBExperience(bot))