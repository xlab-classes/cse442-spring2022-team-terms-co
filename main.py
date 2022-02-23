import keep_alive
import os

import discord
intents = discord.Intents.default()
intents.members = True  
client= discord.Client(intents=discord.Intents.all())

TOKEN = os.environ.get('nTtb1OHEpWat7pkKkMTKTDTP3fLQ6Np9')


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.send('hi')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


keep_alive.keep_alive()
client.run(TOKEN)