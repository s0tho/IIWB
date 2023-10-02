import asyncio
import threading
import logging
from discord.ext import commands
from iiwb.core import utils
from slack_bolt import App
from slack_sdk.web import WebClient
import json
import requests

class SlackCog(commands.Cog):
	def __init__(self, bot):
		"""Initializes Slack bot

		Parameters
		----------
		bot : cog
		"""
		self.bot = bot
		try:
			self.config = utils.load_backend()
		except:
			self.config = None
		slack = self.config.get("tokens").get("slack")
		discord = self.config.get("tokens").get("discord")
		self.slack_token = slack["token"]
		self.slack_signing = slack["signing"]
		self.slack_channel_id = slack["channel_id"]
		self.discord_channel_id = discord["channel_id"]
		self.discord_webhook_url = discord["webhook_url"]

		# Initialize Slack app
		self.slack_app = App(token=self.slack_token, signing_secret=self.slack_signing)
		self.slack_client = WebClient(token=self.slack_token)

		# Start the Slack app in a separate thread
		self.slack_thread = threading.Thread(target=self.run_slack_app)
		self.slack_thread.daemon = True # Dies when main thread (only non-daemon thread) exits.

		self.slack_thread.start()

	def run_slack_app(self):
		"""Start the Slack app"""
		self.slack_app.start(3000)

	@commands.Cog.listener()
	async def on_message(self, message):
		"""Send the Discord message content to Slack

		Parameters
		----------
		message : Message
			Received message from Discord
		"""
		if not message.author.bot:
			if message.channel.id == 1157398462506205184:
				self.send_to_slack(message.content)
		else:
			print(f"Bot: {message.content}")

	def send_to_slack(self, message):
		"""Send the message to Slack

		Parameters
		----------
		message : Message
			Message received from on_message
		"""
		try:
			self.slack_client.chat_postMessage(channel=self.slack_channel_id, text=message)
		except Exception as e:
			print(f"Error sending message to Slack: {e}")

def send_to_discord(message):
	"""Send the message to Discord

	Parameters
	----------
	message : Message
		Received from Slack
	"""
	payload = {'content': message}
	headers = {'Content-Type': 'application/json'}
	response = requests.post("https://canary.discord.com/api/webhooks/1157670604871315487/eTFZ4tsaH7jpmEgyZiX-5iK7JbSeQBNW_JfU_M56e9-ZNDLOkyWZPRu97N3oDyHe89Tz", data=json.dumps(payload), headers=headers)
	
	# Check for errors, successfully sent == 204
	if response.status_code == 204:
		pass
	elif response.status_code == 429:
		print("Rate limited. Please wait before sending more messages.")
	else:
		print(f"Error sending message to Discord. Status code: {response.status_code}, Response: {response.text}")

async def setup(bot):
	# Add the cog
	cog = SlackCog(bot)
	await bot.add_cog(cog)

	@cog.slack_app.event("message")  # Fix here
	def handle_slack_message(event, say):
		# Send message to discord
		channel_id = event.get("channel")
		user_id = event.get("user")
		text = event.get("text")
		send_to_discord(text)
