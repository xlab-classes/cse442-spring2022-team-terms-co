
import keep_alive
import os
import random
import re
import discord


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

#Read the private key from a local file
TOKEN = 'OTQ1ODQxNjU3MTkzMDQxOTcw.YhWBrw.qORMj_xTcO6WswPl5toLDXcDiWo'
toDos = {0: 0}
completed = {}
#toDos =  { taskID: (task_details, tim_e) }
#completed =  { taskID: (task_details, tim_e) }

replies = [
    "Great ", "Awesome ", "Good going! ", " Attayou! ", "What a champ! ",
    "Rest assured! ", "Noted! "
]

@client.event
async def on_ready():
    print(client.user.name, ' has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.channel.send('hi')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
# Snigdha's code:********************************************************************************************************
    #add task
    if message.content.startswith('remind me to') and ' at' in message.content:
        split_index = message.content.find(' at')
        print(split_index)
        tim_e = message.content[split_index + 3:].replace(' ','')
        print(tim_e)
        #.*([0-9]\s?[AM|am|PM|pm]+)
        # time format to handle 5 : 15am
        matched = re.match(".*([0-9]\s?[AM|am|PM|pm]+)", tim_e)
        print(matched)
        is_match = bool(matched)
        if not is_match:
            await message.channel.send(
                "Invalid format. Send a message 'help' for assistance with valid formats."
            )
            return
        print(tim_e)
        toDos[0] += 1
        print(toDos, " counter incremented")
        taskID = toDos[0]
        print(taskID, " task ID")
        toDos[taskID] = (message.content[13:split_index], tim_e)
        print(toDos)
        await message.channel.send(replies[random.randrange(len(replies))])
#***********************************************************************************************************************

# Tanvie's code:********************************************************************************************************
    # delete task
    elif message.content.startswith('delete '):
        split_index = 7
        print(split_index)
        to_del = message.content[split_index:]
        #the task ID to delete is to_del
        print(to_del)
        if not to_del.isdigit():
            await message.channel.send(
                "Invalid format. Send a message 'help' for assistance with valid formats."
            )
        elif int(to_del) in toDos:
            toDos.pop(int(to_del.strip()))
            await message.channel.send("You have successfully deleted a task!")
        else:
            await message.channel.send("No such task exists")
            return
        print(toDos)
#***********************************************************************************************************************

# Mike's code:**********************************************************************************************************
    #completed task:
    elif 'completed' in message.content:
        message_id = int(message.content[message.content.find(' id=') + 4:])
        print("ID completed: ", message_id)
        m = "Congrats on completing task: " + str(message_id)
        completed_task = toDos.pop(message_id)
        completed[message_id] = completed_task
        print(completed)
        await message.channel.send(m)
#***********************************************************************************************************************

# Elijah's code:********************************************************************************************************
    #view task:
    elif message.content.startswith('view'):
        ids = (list(toDos))
        completed_ids = (list(completed))
        #await message.channel.send('you have '+ str(len(ids)-1) +' tasks in progress and '+ str(len(completed_ids)) +' tasks completed')
        # await message.channel.send('In Progress:')
        ip = ''
        comp =''
        if len(ids) <=1:
            await message.channel.send("No tasks in progress type 'help' to learn how to add a task!")
        else:    
            for id in ids[1:]:
                ip+='➼ ID:' + str(id) + '| '+ toDos[id][0]+' at '+ toDos[id][1]+'\n'
            await message.channel.send('In Progress:\n'+ip)
        if len(completed_ids) <=0:
            await message.channel.send("No completed tasks type 'help' to learn how to complete a task!")
        else:    
            for cid in completed_ids:
                comp+='➼ ID:' + str(cid) + '| '+ completed[cid][0]+' at '+ completed[cid][1]+'\n'
            await message.channel.send('Completed:\n' +comp)

#***********************************************************************************************************************

# Rami's code:**********************************************************************************************************
    #edit task:
    elif message.content.startswith('edit'):
        debug = False                                           # if debugging, make True
        if debug: print('Before:')                              # debug
        if debug: print(toDos)                                  # debug
        user_msg = message.content
        if debug: print(user_msg)                               # debug
        splited_sentence = user_msg.split()                     # split the user message into a list
        if splited_sentence[0].lower() in ["edit", "!edit"]:
            task_ID = splited_sentence[1]                       # get the task_ID of the task-to-edit
            if task_ID.isdigit():                               # check task_ID is an int
                task_ID = int(splited_sentence[1])
                if task_ID not in toDos.keys():                 # if task_ID not in toDos then edit no task and warn user
                    await message.channel.send('no task is associated with the ID ', task_ID,    ' :dizzy_face:')
                    return
                else:
                    if debug: print('there is a task associated with the ID ', task_ID)  # debug
                    new_task = ''                                 # store the new task
                    time_idx = 0                                  # specifies the index of time in splited_sentence

                    # get the task details and the time
                    for i in range(3, len(splited_sentence)):
                        if splited_sentence[i] == 'at':
                            time_idx = i + 1  # time always comes after 'at'
                            break
                        else:
                            new_task += splited_sentence[i] + ' '

                    time = splited_sentence[time_idx]

                    # before storing the time to toDos, check if it is formatted correctly:
                    matched = re.match(".*([0-9]\s?[AM|am|PM|pm]+)", time)
                    is_match = bool(matched)
                    if is_match:
                        edited_entry = (new_task, time)
                        toDos[task_ID] = edited_entry              # new entry is entered as a tuple
                    else:
                        await message.channel.send('Your edit message is not formatted correctly.' +
                        '\nYou are probably missing an "at" before your task time.' +
                        '\nType "help" to see how to edit your tasks.       :eyes:')
                        return
            else:
                await message.channel.send('Your edit message is not formatted correctly. Type help.    :eyes:')
                return
        if debug: print('After:')  # debug = just to show the task has been edited
        if debug: print(toDos)  # debug - just to show the task has been edited
        await message.channel.send('your task has been edited   🙂')
#***********************************************************************************************************************

# Rami's code:**********************************************************************************************************
    elif message.content.startswith('help'):
        embed = discord.Embed(
            title="Help",
            description="I support the following commands:\n"
            ":one: " + "add a task by typing \"remind me to \'task\' at \'time\'\n" +
            ":two: " + "delete a task by typing \"delete task_ID\"\n" +
            ":three: " + "edit a task by typing \"edit task_ID : new_task task_time\", make sure there are no spaces in the time (9:00pm) for example \"edit 1 : remind me to sleep at 9pm\"\n" +
            ":four: " + "check all tasks you completed by typing \"completed id=taskid\"\n" +
            ":five: " + "view all tasks you scheduled by typing \"view\"\n" +
            ":bulb: " + "do you know that you can get any task_ID by typing \"view\"",
            color=0xFF5733)
        await message.add_reaction("👍🏾")
        await message.channel.send(embed=embed)
#***********************************************************************************************************************
    else:
        await message.channel.send(
            "Invalid format. Send a message 'help' for assistance with valid formats."
        )

keep_alive.keep_alive()
client.run(TOKEN)
