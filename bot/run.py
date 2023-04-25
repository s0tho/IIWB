import discord
import os
from discord.ext import commands


class MyClient(discord.Client):
    async def on_ready(self):    
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        print(f'{message.created_at} - {message.guild}/{message.channel} - {message.author}: {message.content}')

    async def on_voice_state_update(self, member, before, after):
        channel_id = member.voice.channel.id
        
        if not before.channel and after.channel:
            print(f'{member} has joined {channel_id}')
        else:
            print(f'{member} has left {channel_id}')
        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('BOT_TOKEN'))
