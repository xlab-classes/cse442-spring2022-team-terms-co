import keep_alive
import os
import random
import re
import discord
import asyncio

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

#Read the private key from a local file
TOKEN = os.environ['TOKEN']
toDos = {0: 0, -1: ''}
completed = {}
#toDos =  { taskID: (task_details, tim_e) }
#completed =  { taskID: (task_details, tim_e) }

replies = [
    "Great ", "Awesome ", "Good going! ", " Attayou! ", "What a champ! ",
    "Rest assured! ", "Noted! "
]

@client.event
@asyncio.coroutine
def on_ready():
    print(client.user.name, ' has connected to Discord!')

@client.event
@asyncio.coroutine
def on_member_join(member):
    yielf from member.send('hi')

@client.event
@asyncio.coroutine
def on_message(message):
    if message.author == client.user:
        return
# Snigdha's code:********************************************************************************************************
    #add task
    regexCheck = re.match(".*(?![remind me to]).+", message.content)
    remindMeCheck = re.match("(.*(?=[R-r]emind me to).*)", message.content)
    if bool(regexCheck) and remindMeCheck:
      if ' at' in message.content:
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
            yield from message.channel.send(
                "Invalid format. Send a message 'help' for assistance with valid formats."
            )
            return
        taskID = toDos[0] + 1
        toDos[0] = taskID
        toDos[-1] = message.content[12:split_index]
        print(toDos)
        print(taskID, " task ID")
        toDos[taskID] = (message.content[13:split_index].strip(), tim_e)
        print(toDos)
        yield from message.channel.send(replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID))
        return
      else:
        split_index = message.content.find(' to')
        task = message.content[split_index + 3:].replace(' ','').strip()
        toDos[-1] = task
        print(toDos)
        yield from message.channel.send(
                "At what time? Example: 9am/9PM/6:13am"
          )
        return
    elif bool(re.match("^[0-9].*[AM|am|PM|pm]+", message.content)):
      print("_____" + message.content)
      print(toDos, " counter incremented")
      #increment task ID for the after part of at case
      taskID = toDos[0] + 1
      toDos[0] = taskID
      print(taskID, " task ID")
      toDos[taskID] = (toDos[-1], message.content)
      print(toDos, " counter incremented")
      yield from message.channel.send(replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID))
      return
        
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
        elif int(to_del) in completed:
            completed.pop(int(to_del.strip()))
            await message.channel.send("You have successfully deleted a task!")
        else:
            await message.channel.send("No such task exists")
            return
        print(toDos)
#***********************************************************************************************************************

# Mike's code:**********************************************************************************************************
    #completed task:
    elif 'completed' in message.content:
      message_id = -1
      id_idx = message.content.find(' task')

      #If the id is not found in the dict then set the flag message id to -1
      if(id_idx != -1):
        message_id = message.content[id_idx+ 5:]
        try:
          message_id = int(message_id)
        except:
          message_id = -1
      if message_id not in toDos:
        message_id = -1

      #If the word task or the message id is not found then tell the user their input was incorrect
      if id_idx == -1 or message_id == -1:
        await message.channel.send("You did not correctly list a task, please call help to see the correct formatting")
      else:
        m = "Congrats on completing task: " + str(message_id)
        completed_task = toDos.pop(message_id)
        completed[message_id] = completed_task
        print(completed)
        await message.channel.send(m)
#***********************************************************************************************************************

# Elijah's code:********************************************************************************************************
    #view task:
    elif message.content.startswith('view'):
        sent =''
        ids = (list(toDos))
        completed_ids = (list(completed))
        todos_len = len(ids)-2
        completed_len= len(completed_ids)
        if todos_len == 1:
            todo_tasks= ' task '
        else:
            todo_tasks=' tasks '
        if completed_len == 1:
            completed_tasks= ' task '
        else:
            completed_tasks=' tasks '            
        view_title='You have '+ str(todos_len) + todo_tasks +'in progress and '+ str(completed_len) + completed_tasks + 'completed'
        ip = ''
        comp =''
        if len(ids) <=2:
            sent ="No tasks in progress type 'help' to learn how to add a task!"
        else:    
            for id in ids[2:]:
                ip+='➼ ID:' + str(id) + '| '+ toDos[id][0]+' at '+ toDos[id][1]+'\n'
                sent = 'In Progress:\n'+ip
        if len(completed_ids) <=0:
            send = "No completed tasks type 'help' to learn how to complete a task!"
        else:    
            for cid in completed_ids:
                comp+='➼ ID:' + str(cid) + '| '+ completed[cid][0]+' at '+ completed[cid][1]+'\n'
            send = 'Completed:\n' +comp
        embed = discord.Embed(
            title =view_title,
            description = sent+'\n'+send,
        color =0x7214E3
        )
        await message.channel.send(embed=embed)

#***********************************************************************************************************************

# Rami's code:-----------------------------------------------------------------------------------------------
    # task: edit
    elif message.content.startswith('edit'):
        debug = False  # if debugging, make True
        if debug: print('Before:')  # debug
        if debug: print(toDos)  # debug
        user_msg = message.content
        if debug: print(user_msg)  # debug
        splited_sentence = user_msg.split()  # split the user message into a list
        if splited_sentence[0].lower() in ["edit", "!edit"]:
            task_ID = splited_sentence[1]  # get the task_ID of the task-to-edit
            if task_ID.isdigit():  # check task_ID is an int
                task_ID = int(splited_sentence[1])
                if task_ID not in toDos.keys():  # if task_ID not in toDos then edit no task and warn user
                    await message.channel.send(f'no task is associated with the ID {task_ID}    :dizzy_face:')
                    return
                else:
                    if debug: print(f'there is a task associated with the ID {task_ID}')  # debug
                    new_task = ''  # store the new task
                    time_idx = 0  # specifies the index of time in splited_sentence

                    # get the task details and the time
                    for i in range(3, len(splited_sentence)):
                        if splited_sentence[i] == 'at':
                            time_idx = i + 1  # time always comes after 'at'
                            break
                        else:
                            new_task += splited_sentence[i] + ' '

                    time = splited_sentence[time_idx].replace(' ', '')

                    if time_idx+1 < len(splited_sentence):
                        if splited_sentence[time_idx+1].lower() == 'am' or splited_sentence[time_idx+1].lower() == 'pm':
                            time += splited_sentence[time_idx+1]

                    if debug : print(time)
                    # before storing the time to toDos, check if it is formatted correctly:
                    matched = re.match(".*([0-9]\s?[AM|am|PM|pm]+)", time)
                    is_match = bool(matched)
                    if is_match:
                        edited_entry = (new_task, time)
                        toDos[task_ID] = edited_entry  # new entry is entered as a tuple
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
    # -----------------------------------------------------------------------------------------------------------

# Rami's code:-----------------------------------------------------------------------------------------------
    # task: help
    elif message.content.lower().startswith('help'):
        embed = discord.Embed(
            title="Help",
            description="I support the following commands:\n"
                        "\n:one: " + "add a task by typing \"remind me to \'task\' at \'time\'\n" +
                        "\n:two: " + "delete a task by typing \"delete task_ID\"\n" +
                        "\n:three: " + "edit a task by typing \"edit task_ID : new_task task_time\" for example \"edit 1 : remind me to sleep at 9 pm\"\n" +
                        "\n:four: " + "check all tasks you completed by typing \"completed\"\n" +
                        "\n:five: " + "view all tasks you scheduled by typing \"view\"\n" +
                        "\n:bulb: " + "did you know that you can get any task_ID by typing \"view\"\n" +
                        "\n:bulb: " + "you can see examples of the commands I support by typing \"examples\"",
            color=0xFF5733)
        await message.add_reaction("👍🏾")
        await message.channel.send(embed=embed)
    # -----------------------------------------------------------------------------------------------------------
    else:
        await message.channel.send(
            "Invalid format. Send a message 'help' for assistance with valid formats."
        )

keep_alive.keep_alive()
client.run(TOKEN)
