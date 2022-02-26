import keep_alive
import os

import discord
import random
intents = discord.Intents.default()
intents.members = True  
client= discord.Client(intents=discord.Intents.all())

#Read the private key from a local file
config= open("config.txt", "r")
tk = config.readline()
TOKEN = tk
config.close()

toDos = {}
completed = {}

replies = [
    "Great ", "Awesome ", "Good going! ", " Attayou! ", "What a champ! ",
    "Rest assured! ", "Noted! "
]

id = 0

#Given a message ID this sends a recieved message
#Additionally remove this message from the TODO list and add it to completed
def completed(message_id):
    print("ID completed: ", message_id)
    m = "Congrats on completing task: " + str(message_id)
    completed_task = toDos.pop(message_id)
    completed[message_id] = completed_task
    return m
    #add the task to completed tasks and remove it from toDos

    
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
        toDos[id] = (message.content[0:split_index], tim_e)
        id+=1
        print(toDos)
        await message.channel.send(replies[random.randrange(len(replies))])
    if '!completed' in message.content:
        completed_message = completed(int(message.content[message.content.find(' id=') + 4:]))
        await message.channel.send(completed_message)

            



keep_alive.keep_alive()
client.run(TOKEN)
