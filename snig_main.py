import keep_alive
import os
import random
import re

import discord
#https://discordpy.readthedocs.io/en/stable/api.html
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

TOKEN = 'OTQ1ODQxNjU3MTkzMDQxOTcw.YhWBrw.jkXtKcI-PfLoaqQgt0MEo9f3A-8'

toDos = {}
#toDos =  { taskID: (task_details, tim_e) } 
#completed =  { taskID: (tim_e, task_details) } 
#view all is how the user gets the ID to interact with the task
#reminders = {time: {taskIDs}}
  # reminder accesses time ->
   # goes through taskIDs and reminds for each task
   # also deletes tasks from both dicts
#user is given task ID upon add too
# edit taskID time/taskname

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
        print(split_index)
        tim_e = message.content[split_index + 3:]
        print(tim_e)
        if tim_e not in toDos.keys():
          toDos[tim_e] = message.content[0:split_index]
        else:
          toDos[tim_e] += ', ' + message.content[0:split_index]
        await message.channel.send(replies[random.randrange(len(replies))])
    print(toDos)


keep_alive.keep_alive()
client.run(TOKEN)
