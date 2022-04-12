from sched import scheduler
from winreg import QueryReflectionKey
from distutils.command.config import config
from unicodedata import name
from pytz import timezone
import keep_alive
import os
import random
import re
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from time_manager import process_input_time
from time_manager import time_to_military
import quotes
import config
from user_message_manager import help_command_message, examples_command_message, tips_command_message, important_task_message, not_important_task_message, view_important_tasks, bot_greeting_msg, edit_important_tasks

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

#Read the private key from a local file
toDos = {0: 0, -1: ''}
completed = {}

user_dict = {}
user_dict_completed = {}
#toDos =  { taskID: (task_details, tim_e) }
#completed =  { taskID: (task_details, tim_e) }

replies = [
    "Great ", "Awesome ", "Good going! ", " Attayou! ", "What a champ! ",
    "Rest assured! ", "Noted! "
]

response_messages = {-1:1,
                     1:quotes.normal,#normal
                     2:quotes.motivate,#motivational
                     3:quotes.casual#casual
                    }
quotes={-1:1,
        1:quotes.cliche,
        2:quotes.motivational,
        3:quotes.funny,
        }
def change_mood(emoji):
    if   emoji == '🙂':
        response_messages[-1] = 1
    elif emoji == '💪':
        response_messages[-1] = 2
    elif emoji == '😎':
        response_messages[-1] = 3

# AsyncIOScheduler() is to be used to send the user messages in real-time:
scheduler = AsyncIOScheduler()          # initialize the scheduler
scheduler.start()                       # start the schedule

async def func(msg, task_details, task_time):
    """
    A function to be added to the scheduler when a job is added. This function sends an embed messagem notifying the
    user of the task they scheduled.
    """
    await client.wait_until_ready()
    await send_embed_message(msg, task_details, task_time)

async def send_embed_message(msg, task_details, task_time):
    tone = response_messages[-1]
    random_message = random.randrange(0,len(response_messages[tone]))
    quote_mood = quotes[-1]
    random_quote = random.randrange(0,len(quotes[quote_mood]))
    emoji = ''
    if   tone == 1:
        emoji = '  🙂'       
    elif tone == 2:
        emoji = '  💪'
    elif tone == 3:
        emoji = '  😎'

    """
        A function to generate an embed message template containing the details of a task previously scheduled
        by the user
    """
    embed = discord.Embed(
        title = response_messages[tone][random_message] + task_details + emoji,
        description= quotes[quote_mood][random_quote],
        color=0xEABBC2)
    await msg.channel.send(embed=embed)

#create a func to delete message
#call it in delete and clear all
def delete(id):
    scheduler.remove_job(id)
    scheduler.print_jobs()



# AsyncIOScheduler() is to be used to send the user messages in real-time:
scheduler = AsyncIOScheduler()          # initialize the scheduler
scheduler.start()                       # start the schedule

async def func(msg, task_details, task_time):
    """
    A function to be added to the scheduler when a job is added. This function sends an embed message notifying the
    user of the task they scheduled.
    """
    await client.wait_until_ready()
    await send_embed_message(msg, task_details, task_time)

async def send_embed_message(msg, task_details, task_time):
    x = response_messages[-1]
    y = random.randrange(0,len(response_messages[x]))
    emoji = ''
    if x == 1:
        emoji = ' 🙂'       
    elif x == 2:
        emoji = ' 💪'
        
    elif x == 3:
        emoji = ' 😎'

    """
        A function to generate an embed message template containing the details of a task previously scheduled
        by the user
    """
    embed = discord.Embed(
        title = response_messages[x][y] + task_details + emoji,
        # description="It's" +task_time+ ' '+response_messages[y] + task_details + "\n"
        #             + "\n"
        #            + ":clock1: " + task_time + "\n",
        color=0xEABBC2)#0x6A5ACD
    #await c.send(embed=embed)
    await msg.channel.send(embed=embed)

#create a func to delete message
#call it in delete and clear all
def delete(id):
    scheduler.remove_job(id)
    scheduler.print_jobs()

 
@client.event
async def on_ready():
    print(client.user.name, ' has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.send('hi')

#Rami's Code for remind
def schedule_job(message , message_time, taskID):
    #print('channel: ' + str(message.channel))
    user_time = process_input_time(message_time)
    military_time = time_to_military(user_time)
    time_hrs = military_time[0] + military_time[1]
    time_mins = military_time[3] + military_time[4]
    task_details = user_dict[message.author.id][taskID][0]
    scheduler.add_job(func, CronTrigger(hour=time_hrs, minute=time_mins, second="0"),(message, task_details, military_time,), id=str(taskID), replace_existing=True)
    #scheduler.print_jobs()
    return

#Deletes a task and returns the message the bot should send to the user
def delete_task(message):
    split_index = 7
    to_del = message.content[split_index:]
    if not to_del.isdigit():
        return "Invalid format. Send a message 'help' for assistance with valid formats."
    elif message.author.id not in user_dict:
        return "You can't delete a task because you have not added any"
    elif int(to_del) not in user_dict[message.author.id]:
        return "A message with that id does not exist"
    elif int(to_del) in user_dict[message.author.id]:
        user_dict[message.author.id].pop(int(to_del.strip()))
        return "Successfully deleted!"

#Places a task from the base dictionary into the completed dictionary
def complete_task(message):
    id_idx = message.content.find(' task')
    if id_idx == -1:
        return "Invalid format please type help to see the valid formats"
    
    message_id = message.content[id_idx+ 5:]
    print("M id: " , message_id)
    print("Message content " , message.content)

    if not message_id.strip().isdigit():
        return "Invalid format please type help to see the valid formats that task is not a digit" 
    
    message_id = int(message_id.strip())

    if message_id not in user_dict[message.author.id]:
        return "You do not have an incomplete task with that number"

    if message.author.id not in user_dict_completed:
            user_dict_completed[message.author.id] = {}
            user_dict_completed[message.author.id][message_id]  = user_dict[message.author.id][message_id]
            user_dict[message.author.id].pop(message_id)

            print("Created completed dict: " , user_dict_completed)
            return "Congrats on completing your first task"
    else:
            user_dict_completed[message.author.id][message_id]  = user_dict[message.author.id][message_id]
            user_dict[message.author.id].pop(message_id)
            print("Added to user dict: " , user_dict_completed)
            return "Task marked as completed!"

#TODO Prints out the tasks in completed and todo
def userview_task(message):
    if message.author.id not in user_dict:
        ids = []
    else:
        ids = (list(user_dict[message.author.id]))

    if message.author.id not in user_dict_completed:
        completed_ids = []
    else:
        completed_ids = (list(user_dict_completed[message.author.id]))
    
    sent =''
  
  
    print("IDS: " , ids)
    print("Completed IDS: " , completed_ids)

    #Get rid of incomplete tasks 
    if -1 in ids:
        ids.remove(-1)

    
    todos_len = len(ids)
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
    if len(ids) == 0:
        sent ="No tasks in progress type 'help' to learn how to add a task!"
    else:    
        for id in ids:
            ip+='•ID:' + str(id) + '| '+ user_dict[message.author.id][id][0]+' at '+ user_dict[message.author.id][id][1]+'\n'
        sent = 'In Progress:\n'+ip

    if len(completed_ids) ==0:
        send = "No completed tasks type 'help' to learn how to complete a task!"
    else:    
        for cid in completed_ids:
            comp+='•ID:' + str(cid) + '| '+ user_dict_completed[message.author.id][cid][0]+' at '+ user_dict_completed[message.author.id][cid][1]+'\n'
        send = 'Completed:\n' +comp
    embed = discord.Embed(
        title =view_title,
        description = sent+'\n'+send,
    color =0x7214E3
    )
   
    return embed

#TODO Prints out the tasks in completed and todo
def view_task(message):
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
            ip+='•ID:' + str(id) + '| '+ toDos[id][0]+' at '+ toDos[id][1]+'\n'
            sent = 'In Progress:\n'+ip
    if len(completed_ids) <=0:
        send = "No completed tasks type 'help' to learn how to complete a task!"
    else:    
        for cid in completed_ids:
            comp+='•ID:' + str(cid) + '| '+ completed[cid][0]+' at '+ completed[cid][1]+'\n'
        send = 'Completed:\n' +comp
    embed = discord.Embed(
        title =view_title,
        description = sent+'\n'+send,
    color =0x7214E3
    )
    return embed

#Add a task using the remind me to keywords
#Put tasks into the -1 key if they do not include a time 
def add_task(message):
    if ' at' in message.content:
        split_index = message.content.find(' at')
        tim_e = message.content[split_index + 3:].replace(' ','')
        matched = re.match(".*([0-9]\s?[AM|am|PM|pm]+)", tim_e)
        is_match = bool(matched)

        if not is_match:
            return "Invalid format. Send a message 'help' for assistance with valid formats."
        
        task = (message.content[13:split_index].strip(), tim_e)
        taskID = toDos[0] + 1
        toDos[0] = taskID
        toDos[-1] = message.content[12:split_index]
        toDos[taskID] = task
        #Mikes Addition $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        if message.author.id not in user_dict:
            user_dict[message.author.id] = {}
            user_dict[message.author.id][taskID]  = task
            print("Created user dict: " , user_dict)
        else:
            user_dict[message.author.id][taskID] = task
            print("Added to user dict: " , user_dict)
        # Rami's Addition Schedule the job
        schedule_job(message, tim_e, taskID)
        return replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID)
    else:
        split_index = message.content.find(' to')
        task = message.content[split_index + 3:].strip()

        #If the time is not added store task in a tuple at key -1 
        if message.author.id not in user_dict:
            user_dict[message.author.id] = {}
            user_dict[message.author.id][-1]  = task
            print("Created user dict timeless: " , user_dict)
        else:
            user_dict[message.author.id][-1] = task
            print("Added to user dict timeless: " , user_dict)
        
        toDos[-1] = task
        print("User Dict without time" , user_dict)

        return "At what time? Example: 9am/9PM/6:13am"

#TODO When a time is sent check to see if is associated with a previous task
def add_task_time(message):
    #increment task ID for the after part of at case
    taskID = toDos[0] + 1
    toDos[0] = taskID
    print(taskID, " task ID")
    toDos[taskID] = (toDos[-1], message.content)

    if message.author.id not in user_dict:
        print("User has no stored tasks")
        return 
    elif user_dict[message.author.id][-1] == "":
        print("No task that needs a time")
        return 
    else:
        user_dict[message.author.id][taskID] = (user_dict[message.author.id][-1], message.content)
        user_dict[message.author.id][-1] = ""
        print("Added the time to user dict: " , user_dict)

    return replies[random.randrange(len(replies))] + ". The task ID(time) is " + str(taskID)
    
   

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    usr_important_message = message.content.split() # parsing user's message for makring tasks as important

    #Add task
    regexCheck = re.match(".*(?![remind me to]).+", message.content)
    remindMeCheck = re.match("(.*(?=[R-r]emind me to).*)", message.content)
    if bool(regexCheck) and remindMeCheck:
        bot_message = add_task(message)
        await message.channel.send(bot_message)
        return
    #Add task if the time was not previously sent
    elif bool(re.match("^[0-9].*[AM|am|PM|pm]+", message.content)):
        bot_message= add_task_time(message)
        await message.channel.send(bot_message)
        return
    #Delete task
    elif message.content.startswith('delete '):
        bot_message = delete_task(message)
        await message.channel.send(bot_message)
        return
    #Completed task
    elif message.content.startswith('completed '):
        bot_message = complete_task(message)
        await message.channel.send(bot_message)
        return
    #view task:
    elif message.content.startswith('userview'):
        bot_message = userview_task(message)
        await message.channel.send(embed= bot_message)
        return 
    elif message.content.startswith('view'):
        bot_message = view_task(message)
        await message.channel.send(embed=bot_message)
    #clear all currently does not work with new dictionary
    elif message.content.startswith('clear all tasks') or message.content.startswith('clear'):
        ids = list(toDos)
        completed_ids = list(completed)
        for i in ids[2:]:
            toDos.pop(i)
            delete(str(i))
        for i in completed_ids:
            completed.pop(i)  
        if len(ids+completed_ids) <=2:
            await message.channel.send("You dont have any tasks to clear 🙃")
        else:
            await message.channel.send("OK all your tasks are cleared 🙂")

#***********************************************************************************************************************
    elif message.content.startswith('change mood'):
        if   '🙂' in message.content:            
            await message.channel.send("mood changed to normal")
            change_mood('🙂')
            print(response_messages[-1])            
        elif '😎' in message.content:                    
            await message.channel.send("mood changed to casual")
            change_mood('😎')
            print(response_messages[-1])            
        elif '💪' in message.content:
            await message.channel.send("mood changed to motivtional")
            change_mood('💪')
            print(response_messages[-1])
        else:
            embed = discord.Embed(
            title ='mood not currently available try one thats below⬇️⬇️',
            description = "\n🙂 for neutral\n"+
                          '\n💪 for motivational\n'+
                          '\n😎 for casual\n',
                color =0x22DB22)
            await message.channel.send(embed=embed)        

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
                        #Mikes addition to edit $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                        if message.author.id not in user_dict:
                            await message.channel.send('You currently have no stored tasks')
                        else:
                            user_dict[message.author.id][task_ID] = edited_entry
                            print("User_dict successfully edited: " , user_dict)
                            await message.channel.send('User Dict was edited succesfully')

                        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # reminder addition: -------------------------------------------------------------------------------------------    
                        user_time = process_input_time(time)

                        military_time = time_to_military(user_time)
                        time_hrs = military_time[0] + military_time[1]
                        time_mins = military_time[3] + military_time[4]

                        # scheduler.reschedule_job() does not allow the change of the message passed to the old job,
                        # so I had to remove and then add the job with a new message
                        scheduler.remove_job(str(task_ID))
                        scheduler.add_job(func, CronTrigger(hour=time_hrs, minute=time_mins, second="0"),
                                          (message, new_task, military_time,), id=str(task_ID))  # old
        # --------------------------------------------------------------------------------------------------------------

                      
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
     # Rami's code:******************************************************************************************************
    # task: tips        # user story: make the bot more user-friendly
    elif message.content.lower().startswith('tips'):
        embed = discord.Embed(
        title="Tips",
            description=tips_command_message(),
        color=0x6A5ACD)
        await message.add_reaction("👍🏾")
        await message.channel.send(embed=embed)
    # ******************************************************************************************************************

    # ******************************************************************************************************************
    # task: Replying to greetings        # user story: make the bot more user-friendly
    elif (message.content.lower().startswith('hey') or
          message.content.lower().startswith('hi') or
          message.content.lower().startswith('hello')):

        await message.add_reaction("👋")
        await message.channel.send(bot_greeting_msg())
    # ******************************************************************************************************************

    # ******************************************************************************************************************
    # Task: Important
    elif (message.content.lower().startswith('mark task') and
          usr_important_message[3].lower() == 'as' and
          usr_important_message[4].lower() == 'important'):

        await message.channel.send(important_task_message(message.content, 2, toDos, important_tasks))
    # ******************************************************************************************************************

    # ******************************************************************************************************************
    # Task: Marking an important task as not important. If the task is not marked as important, then it will not be
    # affected. Assume the correct user message format is: "mark task task_ID as not important"
    elif (message.content.lower().startswith('mark task') and
          usr_important_message[3].lower() == 'as' and
          usr_important_message[4].lower() == 'not' and
          usr_important_message[5].lower() == 'important'):

          await message.channel.send(not_important_task_message(message.content, 2, important_tasks))
    # ******************************************************************************************************************

    # ******************************************************************************************************************
    # Task: Viewing all Important tasks.
    elif (message.content.lower().startswith('list important tasks')):
        embed = discord.Embed(
            title="Important Tasks",
            description=view_important_tasks(important_tasks),
            color=0xFF0000) # red
        await message.channel.send(embed=embed)
    # ******************************************************************************************************************

    else:
        await message.channel.send(
            "Invalid format. Send a message 'help' for assistance with valid formats."
        )

keep_alive.keep_alive()

if __name__ == '__main__':
    import config
    client.run(config.token)