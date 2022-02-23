import keep_alive
import os

import discord
import random
intents = discord.Intents.default()
intents.members = True  
client= discord.Client(intents=discord.Intents.all())

#Dont commit the private key
'''
config= open("config.txt")
TOKEN = os.environ.get(config.readline(32))
config.close()
'''
TOKEN = 'OTQ1NDEwNzA4ODQ4Mzg2MTY5.YhPwVQ.DCbY-M9IT83w54wEK7lsSViKznw'


toDos = {}
completed = {}

replies = [
    "Great ", "Awesome ", "Good going! ", " Attayou! ", "What a champ! ",
    "Rest assured! ", "Noted! "
]

id = 0

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
        #for this to work id must be at the end of the message 

        id_completed = int(message.content[message.content.find(' id=') + 4:])
        print("ID completed: ", id_completed)
        m = "Congrats on completing task: " + str(id_completed)
        await message.channel.send(m)

        #add the task to completed tasks and remove it from toDos
        '''
        completed[id_completed] = toDos.pop(id_completed)

        #TODO add randomized messages
        message.channel.send("Congrats on completing task: " , id_completed)
        '''
            



keep_alive.keep_alive()
client.run(TOKEN)