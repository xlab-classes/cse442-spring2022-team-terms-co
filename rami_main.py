# import keep_alive # not needed for demo


import random
import re
import discord

client = discord.Client()

TOKEN = ''

toDos = {'4pm' : 'remind me to eat'}  # initialized with Snighda's test value

replies = [
    "Great ", "Awesome ", "Good going! ", " Attayou! ", "What a champ! ",
    "Rest assured! ", "Noted! "
]


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')  # Snighda's code


@client.event
async def on_member_join(member):
    await member.send('hi')   # Snighda's code
    await member.send('hi. The following are the list of commands I currently support: ',
                      '1. type "remind me to" to schedule an event.',
                      '2. type "!edit #_of_event: #your_edit" to edit an event.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Snighda's code:--------------------------------------------------------------------------------------------
    if 'remind me to' in message.content and not (message.content.startswith('!edit')):
        split_index = message.content.find(' at')
        print(split_index)
        tim_e = message.content[split_index + 3:]
        print(tim_e)
        toDos[tim_e] = message.content[0:split_index]
        print(toDos)
        await message.channel.send(replies[random.randrange(len(replies))])
    # -----------------------------------------------------------------------------------------------------------

    # Rami's code:-----------------------------------------------------------------------------------------------
    if message.content.startswith('!edit'):
        print('Before:')                                                # just to show the task has been edited
        print(toDos)                                                    # just to show the task has been edited
        str = message.content.rsplit(':', 1)
        time = (str[0][len(str[0]) - 4: len(str[0])]).rstrip()          # get the time of the task being edited
        new_task = str[1].lstrip()                                      # get the new task
        toDos[time] = new_task                                          # reflect the changes in the dictionary
        print('After:')                                                 # just to show the task has been edited
        print(toDos)                                                    # just to show the task has been edited
        await message.channel.send('your task has been edited')
    # -----------------------------------------------------------------------------------------------------------


# that is my bot token
client.run('OTQ2MDM5MzAwMTQ1OTQyNTkw.YhY5wQ.Qomyfnt6iQR3OWpValfDxKi09es')
