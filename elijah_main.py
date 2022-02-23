import keep_alive
import os
import random
import re

import discord
#https://discordpy.readthedocs.io/en/stable/api.html
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

TOKEN = 'OTQ1ODc3NjkyNjczMzE4OTYz.YhWjPw.i4K8R-9eayki3LahCqWapaVsSqs'

toDos = {}
Completed = {}


replies = [
    "Great ", "Awesome ", "Good going! ", " Attayou! ", "What a champ! ",
    "Rest assured! ", "Noted! "
]


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
    if 'remind me to' in message.content:
        split_index = message.content.find(' at')
        #print(split_index)
        tim_e = message.content[split_index + 3:].strip()
        #print(tim_e)
        toDos[tim_e] = message.content[13:split_index]
        #print(toDos)
        await message.channel.send(replies[random.randrange(len(replies))])
    if message.content.startswith('!view'):
        await message.channel.send('You have '+str(len(toDos))+' task in progress and '+str(len(Completed)) +' tasks completed:'+'\n\nIn Progress:')
        for key, value in toDos.items():
            #print(value, 'at', key)
            await message.channel.send('  ➼'+value + ' at ' + key)
        await message.channel.send('Completed:')
        

keep_alive.keep_alive()
client.run(TOKEN)
