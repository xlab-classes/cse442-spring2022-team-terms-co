import keep_alive
import os
import re
import discord
import random

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

#Read the private key from a local file
TOKEN = os.environ['TOKEN']
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
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.send('hi')




@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #add task
    if message.content.startswith('remind me to') and ' at' in message.content:
        split_index = message.content.find(' at')
        print(split_index)
        tim_e = message.content[split_index + 3:]
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
        toDos[taskID] = (message.content[0:split_index], tim_e)
        print(toDos)
        await message.channel.send(replies[random.randrange(len(replies))])

    #delete taskID
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

    #complete
    elif 'completed' in message.content:
        message_id = int(message.content[message.content.find(' id=') + 4:])
        print("ID completed: ", message_id)
        m = "Congrats on completing task: " + str(message_id)
        completed_task = toDos.pop(message_id)
        completed[message_id] = completed_task
        print(completed)
        await message.channel.send(m)
      
    #view
    elif message.content.startswith('view'):
        await message.channel.send('In Progress:')
        for key, value in toDos.items():
            #print(value, 'at', key)
            #toDos =  { taskID: (task_details, tim_e) }
            await message.channel.send('  ➼' + str(value) + ' at ' + str(key))
        await message.channel.send('Completed:')

    # Rami's code:-----------------------------------------------------------------------------------------------
    elif message.content.startswith('edit'):
        # print('Before:')  # debug
        # print(toDos)  # debug
        user_msg = message.content
        # print(user_msg)  # get the user message
        splited_sentence = user_msg.split(
        )  # split the user message into a list
        if splited_sentence[0].lower() in [
                "edit", "!edit"
        ]:  # check that the user message is an edit request
            task_ID = splited_sentence[
                1]  # get the task_ID of the task-to-edit
            if task_ID.isdigit():  # check task_ID is an int
                task_ID = int(splited_sentence[1])
                if task_ID not in toDos.keys(
                ):  # if task_ID not in toDos then edit no task and warn user
                    await message.channel.send(
                        f'no task is associated with the ID {task_ID}    :dizzy_face:'
                    )
                    return
                else:
                    print(f'there is a task associated with the ID {task_ID}'
                          )  # debug
                    print(toDos)
                    new_task = ''  # store the new task
                    time_idx = 0  # specifies the index of time in splited_sentence

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
                        toDos[
                            task_ID] = edited_entry  # new entry is entered as a tuple
                    else:
                        await message.channel.send(
                            'The time format you inputted is not correct    :eyes:'
                        )
                        return
            else:
                await message.channel.send(
                    'The time format you inputted is not correct    :eyes:')
                return
        print('After:')  # debug = just to show the task has been edited
        print(toDos)  # debug - just to show the task has been edited
        await message.channel.send('your task has been edited   🙂')
    # -----------------------------------------------------------------------------------------------------------
    #help:
    # Rami's code:----------------------------------------------------------------------------------------------


# Rami's code:-----------------------------------------------------------------------------------------------
    elif message.content.startswith('help'):
        embed = discord.Embed(
            title="Help",  #url="https://realdrewdata.medium.com/",
            description="I support the following commands:\n"
            ":one: " + "edit to edit an existing task\n" + ":two: " +
            " 'remind me to...at' add a new task\n" + ":three: " +
            "view all to see all the tasks you scheduled\n",
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
