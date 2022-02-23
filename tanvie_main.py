import keep_alive
import os
import random
import re

import discord
#https://discordpy.readthedocs.io/en/stable/api.html
intents = discord.Intents.default()
intents.members = True
#client = discord.Client(intents=discord.Intents.all())

client = discord.Client()
TOKEN = 'OTQ1OTIwMzAzNDU0OTAwMzE0.YhXK7g.nW0YSawjElFDoAFhGmEsBDf6qT8'

toDos = {}

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
    if message.content.startswith('remind me to'):
        split_index = message.content.find(' at ')
        print(split_index)
        tim_e = message.content[split_index + 3:]
        print(tim_e)
        toDos[message.content[0:split_index].strip()] = tim_e.strip()
        print(toDos)
        await message.channel.send(replies[random.randrange(len(replies))])

    elif message.content.startswith('delete '):
        split_index = 7
        print(split_index)
        to_del = message.content[split_index:]
        print(to_del)
        if to_del in toDos:
          toDos.pop(to_del.strip())
        else:
          await message.channel.send("No such task exists")
          return
        print(toDos)
        await message.channel.send("You have successfully deleted a task!")

keep_alive.keep_alive()
client.run(TOKEN)
