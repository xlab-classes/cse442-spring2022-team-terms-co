from distutils.command.config import config
from turtle import update
import keep_alive
import random
import re
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord_components import SelectOption, Select, DiscordComponents
from time_manager import process_input_time
from time_manager import time_to_military
import quotes
import config
import json
from user_message_manager import help_command_message, examples_command_message, tips_command_message, important_task_message, not_important_task_message, view_important_tasks, bot_greeting_msg, edit_important_tasks

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/')      # new

#Read the private key from a local file
toDos = {0: 0, -1: ''}
completed = {}

user_dict = {}
user_dict_completed = {}
user_dict_overdue ={}
#toDos =  { taskID: (task_details, tim_e) }
#completed =  { taskID: (task_details, tim_e) }

important_tasks = {}  # important_tasks = {taskID : "task_details + time" }

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
        quotes[-1] = 1
    elif emoji == '💪':
        response_messages[-1] = 2
        quotes[-1] = 2
    elif emoji == '😎':
        response_messages[-1] = 3
        quotes[-1] = 3

# AsyncIOScheduler() is to be used to send the user messages in real-time:
scheduler = AsyncIOScheduler()          # initialize the scheduler
scheduler.start()                       # start the schedule

async def func(msg, task_details, task_time, taskID):
    """
    A function to be added to the scheduler when a job is added. This function sends an embed message notifying the
    user of the task they scheduled.
    """
    add_to_overdue(msg, taskID)
    await bot.wait_until_ready()
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

#Removes a task from in progress and adds it to overdue
def add_to_overdue(msg, taskID):
    if msg.author.id not in user_dict:
        return "Author has no Dictionary"
    
    if taskID not in user_dict[msg.author.id]:
        print("The task was already completed so no need to move it to overdue")
        return "This user has no stored messages"
    
    overdue_task = user_dict[msg.author.id].pop(taskID)

    if msg.author.id not in user_dict_overdue:
        user_dict_overdue[msg.author.id] = {}
        user_dict_overdue[msg.author.id][taskID] = overdue_task
        print("Overdue Dict Created: " , user_dict_overdue) 

    else:
        user_dict_overdue[msg.author.id][taskID] = overdue_task
        print("Overdue Dict : " , user_dict_overdue) 
    return "Added to overdue"
#call it in delete and clear all
def delete(id):
    scheduler.remove_job(id)
    scheduler.print_jobs()
 
@bot.event
async def on_ready():
    DiscordComponents(bot)  # new
    print(bot.user.name, ' has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.send('hi')
    
# Enabling a drop-down menu to list the commands supported by the bot:
@bot.command()
async def commands(ctx):  # new
    if ctx.author.id == 670325098598629377 or 426376741028888576:
        await ctx.send(
            components=[
                Select(
                    placeholder='Supported Commands',
                    options=[
                        SelectOption(label="schedule a task", description="type: remind me to 'task details' at 'task time'",
                                     value="value1"),
                        SelectOption(label="delete a task", description="type: delete 'task_ID'", value="value2"),
                        SelectOption(label="edit a task", description="type: edit 'task_ID' : 'new task details' at 'new task time' ",
                                     value="value3"),
                        SelectOption(label="view your schedule", description="type: view", value="value4"),
                        SelectOption(label="make a task important", description="type: mark task 'task_ID' as important",
                                     value="value5"),
                        SelectOption(label="remove important tag",
                                     description="type: mark task 'task_ID' as not important", value="value6"),
                        SelectOption(label="get help", description='type: help', value="value7"),
                        SelectOption(label="clear your schedule", description='type: clear all', value="value8"),
                        SelectOption(label="view your important tasks", description='type: list important tasks',
                                     value="value9"),
                        SelectOption(label="see examples of the commands", description='type: examples',
                                     value="value10")
                    ])])


# Specifying the events that take place when the user interacts with the /commands drop-down menu:
@bot.event
async def on_select_option(interaction):  # new
    # await interaction.respond(type=6)
    if interaction.values[0] == "value1":
        await interaction.send("type: remind me to 'task details' at 'task time'")
    elif interaction.values[0] == "value2":
        await interaction.send("type: delete 'task_ID'")
    elif interaction.values[0] == "value3":
        await interaction.send("type: edit 'task_ID' : 'new task details' at 'new task time' ")
    elif interaction.values[0] == "value4":
        await interaction.send('type: view')
    elif interaction.values[0] == "value5":
        await interaction.send("type: mark task 'task_ID' as important")
    elif interaction.values[0] == "value6":
        await interaction.send("type: mark task 'task_ID' as not important")
    elif interaction.values[0] == "value7":
        await interaction.send('type: help')
    elif interaction.values[0] == "value8":
        await interaction.send('type: clear all')
    elif interaction.values[0] == "value9":
        await interaction.send('type: list important tasks')
    elif interaction.values[0] == "value10":
        await interaction.send('type: examples')
    else:
        await interaction.respond(type=6)
    

#Rami's Code for remind
def schedule_job(message , message_time, taskID):
    user_time = process_input_time(message_time)
    military_time = time_to_military(user_time)
    time_hrs = military_time[0] + military_time[1]
    time_mins = military_time[3] + military_time[4]
    task_details = user_dict[message.author.id][taskID][0]
    scheduler.add_job(func, CronTrigger(hour=time_hrs, minute=time_mins, second="0"),(message, task_details, military_time, taskID,), id=str(taskID), replace_existing=True)
    return

#Deletes a task and returns the message the bot should send to the user
def delete_task(message):
    split_index = 7
    to_del = message.content[split_index:]
    if not to_del.isdigit():
        embed = discord.Embed(
        title ="Unable to delete that task. To delete a task send it in the format below:",
        description = 'delete task_ID\n \n ex:\n delete 4',
        color =0xeb34c9
        )   
        return embed
    elif message.author.id not in user_dict:
        embed = discord.Embed(
        title ="You have no current tasks to delete",
        color =0xeb34c9
        )   
        return embed        
    elif int(to_del) not in user_dict[message.author.id] and int(to_del) not in user_dict_completed[message.author.id]:
        embed = discord.Embed(
        title ="A task with that id does not exist",
        description = 'delete task_ID\n \n ex:\n delete 4',
        color =0xeb34c9
        )   
        return embed        
    elif int(to_del) in user_dict[message.author.id]:
        user_dict[message.author.id].pop(int(to_del.strip()))
        important_tasks.pop(int(to_del.strip()))  # new
        embed = discord.Embed(
        title ="Successfully deleted!",
        color =0xeb34c9
        )   
        return embed        
    elif int(to_del) in user_dict_completed[message.author.id]:
        user_dict_completed[message.author.id].pop(int(to_del.strip()))
        important_tasks.pop(int(to_del.strip()))  # new
        embed = discord.Embed(
        title ="Successfully deleted!",
        color =0xeb34c9
        )   
        return embed 
#Places a task from the base dictionary into the completed dictionary
def complete_task(message):
    id_idx = message.content.find(' task')
    if id_idx == -1:
        embed = discord.Embed(
        title ="Invalid format. To complete a task send it in the format below:",
        description = "Completed task task_ID\n \n"+'ex:\n completed task 4',
        color =0x4e03fc
        )    
        return embed
    
    message_id = message.content[id_idx+ 5:]
    print("M id: " , message_id)
    print("Message content " , message.content)

    if not message_id.strip().isdigit():
        embed = discord.Embed(
        title ="Task id not found. To complete a task send it in the format below:",
        description = "Completed task task_ID\n \n"+'ex:\n completed task 4',
        color =0x4e03fc
        )    
        return embed        

    message_id = int(message_id.strip())

    if message.author.id not in user_dict and message.author.id not in user_dict_overdue:
        embed = discord.Embed(
        title ="You have no overdue or in progress tasks",
        color =0x4e03fc
        )    
        return embed
    
    if message.author.id in user_dict and message.author.id not in user_dict_overdue:
        if message_id not in user_dict[message.author.id]:
            embed = discord.Embed(
            title ="The task with this ID has either already been completed or has been deleted",
            color =0x4e03fc
            )    
            return embed
    if message.author.id in user_dict_overdue and message.author.id not in user_dict:
        if message_id not in user_dict_overdue[message.author.id]:
            embed = discord.Embed(
            title ="The task with this ID has has either already been deleted or completed",
            color =0x4e03fc
            )    
            return embed

    if message_id in user_dict[message.author.id]:
        if message.author.id not in user_dict_completed:
            user_dict_completed[message.author.id] = {}
            user_dict_completed[message.author.id][message_id]  = user_dict[message.author.id][message_id]
            user_dict[message.author.id].pop(message_id)

            print("Created completed dict: " , user_dict_completed)
            embed = discord.Embed(
            title ="Congrats on completing your task!",
            color =0x4e03fc
            )    
            return embed      
        else:
            user_dict_completed[message.author.id][message_id]  = user_dict[message.author.id][message_id]
            user_dict[message.author.id].pop(message_id)
            print("Added to user dict: " , user_dict_completed)
            embed = discord.Embed(
            title ="Task marked as completed",
            color =0x4e03fc
            )    
            return embed        
    if message_id in user_dict_overdue[message.author.id]:
        if message.author.id not in user_dict_completed:
            user_dict_completed[message.author.id] = {}
            user_dict_completed[message.author.id][message_id]  = user_dict_overdue[message.author.id][message_id]
            user_dict_overdue[message.author.id].pop(message_id)

            print("Created completed dict: " , user_dict_completed)
            embed = discord.Embed(
            title ="Congrats on completing your task!",
            color =0x4e03fc
            )    
            return embed      
        else:
            user_dict_completed[message.author.id][message_id]  = user_dict_overdue[message.author.id][message_id]
            user_dict_overdue[message.author.id].pop(message_id)
            print("Added to user dict: " , user_dict_completed)
            embed = discord.Embed(
            title ="Task marked as completed",
            color =0x4e03fc
            )    
            return embed        
    return discord.Embed(title ="No task with this ID exists for your account",color =0x4e03fc)    

    

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
  

    if message.author.id not in user_dict_overdue:
            overdue_ids = []
    else:
            overdue_ids = (list(user_dict_overdue[message.author.id]))
        
  
    print("IDS: " , ids)
    print("Completed IDS: " , completed_ids)
    print("Overdue IDs " , overdue_ids)

    #Get rid of incomplete tasks 
    if -1 in ids:
        ids.remove(-1)

    
    todos_len = len(ids)
    completed_len= len(completed_ids)
    overdue_len = len(overdue_ids)
    if todos_len == 1:
        todo_tasks= ' task '
    else:
        todo_tasks=' tasks '

    if completed_len == 1:
        completed_tasks= ' task '
    else:
        completed_tasks=' tasks '   

    if overdue_len == 1:
        overdue_tasks= ' task '
    else:
        overdue_tasks=' tasks '    

    view_title=('Hey '+  message.author.name + ' you have '
    + str(todos_len) + todo_tasks +'in progress and '
    + str(completed_len) + completed_tasks + 'completed and '
    + str(overdue_len) + overdue_tasks + ' overdue')

    ip = ''
    comp =''
    d = ''
    if len(ids) == 0:
        sent ="No tasks in progress type 'help' to learn how to add a task!"
    else:    
        for id in ids:
            if id in important_tasks:
                ip += '•ID:' + str(id) + '| :red_circle: ' + user_dict[message.author.id][id][0] + ' at ' + user_dict[message.author.id][id][1] + '\n'
            # ------------------------------------------------------------------------------------------------------
            else:             
                ip+='•ID:' + str(id) + '| '+ user_dict[message.author.id][id][0]+' at '+ user_dict[message.author.id][id][1]+'\n'
            sent = 'In Progress:\n'+ip

    if len(completed_ids) ==0:
        send = "No completed tasks type 'help' to learn how to complete a task!"
    else:    
        for cid in completed_ids:
            comp+='•ID:' + str(cid) + '| '+ user_dict_completed[message.author.id][cid][0]+' at '+ user_dict_completed[message.author.id][cid][1]+'\n'
        send = 'Completed:\n' +comp

    if len(overdue_ids) ==0:
        due = "No tasks are overdue, good job!"
    else:    
        for did in overdue_ids:
            d+='•ID:' + str(did) + '| '+ user_dict_overdue[message.author.id][did][0]+' at '+ user_dict_overdue[message.author.id][did][1]+'\n'
        due = 'Overdue:\n' +d 

    embed = discord.Embed(
        title =view_title,
        description = sent+'\n'+send + '\n' + due,
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
        are_is = 'is '
    else:
        todo_tasks=' tasks '
        are_is = 'are '
        
    if completed_len == 1:
        completed_tasks= ' task '
    else:
        completed_tasks=' tasks '       

    view_title='There '+ are_is+ str(todos_len) + todo_tasks +'in progress and '+ str(completed_len) + completed_tasks + 'completed'
    ip = ''
    comp =''
    if len(ids) <=2:
        sent ="No tasks in progress type 'help' to learn how to add a task!"
    else:    
        for id in ids[2:]:
            if id in important_tasks:
                ip += '•ID:' + str(id) + '| :red_circle: ' + toDos[id][0] + ' at ' + toDos[id][1] + '\n'
            # ------------------------------------------------------------------------------------------------------
            else:            
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
            
            embed = discord.Embed(
            title ="Unable to add the task. To add a task send a message in the following format:",
            description = 'remind me to do a task at time\n \n ex:\n remind me to cook dinner at 5:30pm',
            color =0xeb34c9
            )   
            return embed
        
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
        embed = discord.Embed(
        title =replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID),
        color =0xeb34c9
        )   
        return embed
        # return replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID)
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
        embed = discord.Embed(
        title ="At what time? Example: 9am/9PM/6:13am",
        color =0xeb34c9
        )   
        return embed

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
    embed = discord.Embed(
    title =replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID),
    color =0xeb34c9
    )   
    return embed
    # return replies[random.randrange(len(replies))] + ". The task ID(time) is " + str(taskID)  

#Puts the contents of the dictionary into the json file
def update_json():

    #Reading in these files serves no purpose im just keeping it here in case we need an example of how to access them
    filename = 'user_data.json'
    with open(filename, "r") as file:
        user_json_data = json.load(file)
    with open("completed_data.json" , "r") as complete_file:
        completed_json_data = json.load(complete_file)
    with open("overdue_data.json", "r") as overdue_file:
        overdue_json_data = json.load(overdue_file)

    if len(user_dict)>0:
        user_json_data= user_dict
        with open(filename, "w") as file:
            json.dump(user_json_data, file)

    if len(user_dict_completed) > 0:
            completed_json_data= user_dict_completed
            with open("completed_data.json", "w") as file:
                json.dump(completed_json_data, file)

    if len(user_dict_overdue) > 0:
            overdue_json_data= user_dict_overdue
            with open("overdue_data.json", "w") as file:
                json.dump(overdue_json_data, file)
    print("Json Files updated")

#Todo a function that updates the changes made on the webapp before running a message sent to the bot
def refresh_json():
    return


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    usr_important_message = message.content.split() # parsing user's message for makring tasks as important

    #Add task
    regexCheck = re.match(".*(?![remind me to]).+", message.content)
    remindMeCheck = re.match("(.*(?=[R-r]emind me to).*)", message.content)
    channelRegexCheck = re.match('[S-s]tart \w*$', message.content)
    if bool(regexCheck) and remindMeCheck:
        bot_message = add_task(message)
        update_json()
        await message.channel.send(embed = bot_message)
        return
    elif message.content.startswith('Start') or message.content.startswith('start') :
      print("--", message.content, "- - ", bool(channelRegexCheck))
      if message.content == 'start!' or message.content == 'Start!':
        channel = await message.guild.create_text_channel('toDos')
        await message.channel.send("New defualt channel: 'todos' to schedule your tasks has been created!")
        return
      elif bool(channelRegexCheck):
        print("btuh")
        channelName = message.content.split(' ')[1]
        print(channelName)
        channel = await message.guild.create_text_channel(channelName)
        await message.channel.send("New channel: ", channelName, " to schedule your tasks has been created!")
        return
      else:
        await message.channel.send("Invalid start format, please type help for format guide")
        return
        

    #Add task if the time was not previously sent
    elif bool(re.match("^[0-9].*[AM|am|PM|pm]+", message.content)):
        bot_message= add_task_time(message)
        if bot_message == 1:
            embed = discord.Embed(
            title ="Unable to add the task. To add a task send a message in the following format:",
            description = 'remind me to do a task at time\n \n ex:\n remind me to cook dinner at 5:30pm',
            color =0xeb34c9
            )   
            await message.channel.send(embed = embed)
            return
        else:
            update_json()
            await message.channel.send( embed = bot_message)
    
    #Delete task
    elif message.content.startswith('delete '):
        bot_message = delete_task(message)
        update_json()
        await message.channel.send(embed = bot_message)
        return
    #Completed task
    elif message.content.startswith('completed '):
        bot_message = complete_task(message)
        update_json()
        await message.channel.send(embed= bot_message)
        return
    #view task:
    elif message.content.startswith('userview'):
        bot_message = userview_task(message)
        await message.channel.send(embed= bot_message)
        return 
    elif message.content.startswith('view'):
        bot_message = userview_task(message)
        await message.channel.send(embed=bot_message)
    #clear all 
    elif message.content.startswith('clear all tasks') or message.content.startswith('clear'):
        ids = list(toDos)
        completed_ids = list(completed)
        user_todo = list(user_dict)
        # print(user_todo)
        user_completed = list(user_dict_completed)
        # print(user_completed)
        for i in ids[2:]:
            toDos.pop(i)
            delete(str(i))
        for i in user_todo:
            del user_dict[i]  
        for i in user_completed:
            del user_dict_completed[i]
        for i in completed_ids:
            completed.pop(i)

        update_json()
        await message.channel.send("OK all your tasks have been cleared 🙂")
        important_tasks.clear()             # NEW

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
    elif message.content.startswith('quote'):
        quote =''
        if   quotes[-1] == 1:    
             random_quote = random.randrange(0,len(quotes[1]))
             quote = quotes[1][random_quote]
             quote_type = "Here's a cliche quote"

        elif quotes[-1] ==2:
             random_quote = random.randrange(0,len(quotes[2]))
             quote = quotes[2][random_quote]
             quote_type = "Here's a Motivational quote"

        elif quotes[-1] ==3:
             random_quote = random.randrange(0,len(quotes[3]))
             quote = quotes[3][random_quote]
             quote_type = "Here's a funny quote"
        embed = discord.Embed(
        title =quote_type,
        description = quote,
            color =0xBBA14F )
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
                    fill =''
                    for key in toDos.keys():
                        if key > 0:
                            fill += str(key)+', '
                    fill = fill[:len(fill)-2]
                    embed = discord.Embed(
                        title ='no task is associated with the ID '+str(task_ID)+'    :dizzy_face:',
                        description = 'These are the current tasks IDs you currently can edit ['+ fill +']\nType view to see more information about your tasks.',
                    color =0x43eb34
                    ) 
                    await message.channel.send(embed=embed)                        
                    # await message.channel.send(f'no task is associated with the ID {task_ID}    :dizzy_face:')
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
                        user_dict[message.author.id][task_ID] = edited_entry
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
                embed = discord.Embed(
                    title ="Your edit message is not formatted correctly. To edit a task send it in the format below:",
                    description = 'edit task task_ID : new_task_details at new_task_time\n \n ex:\n edit task 4 : meal prep at 4:45pm \n HINT: dont forget the spaces around the colon',
                color =0x43eb34
                ) 
                await message.channel.send(embed=embed)               
                    
                return
        if debug: print('After:')  # debug = just to show the task has been edited
        if debug: print(toDos)  # debug - just to show the task has been edited
        update_json()
        await message.channel.send('your task has been edited   🙂')
    # -----------------------------------------------------------------------------------------------------------

    # Rami's code:******************************************************************************************************
    # task: help
    elif message.content.lower().startswith('help'):
        embed = discord.Embed(
            title="Help",
            description=help_command_message(),
            color=0xFF5733)
        await message.add_reaction("👍🏾")
        await message.channel.send(embed=embed)
    # ***

    # Rami's code:******************************************************************************************************
    # task: example
    elif message.content.lower().startswith('examples') or message.content.lower().startswith('example'):
        embed = discord.Embed(
        title="Examples of Commands I support",
        description=examples_command_message(),
        color=0x6A5ACD)
        await message.add_reaction("👍🏾")
        await message.channel.send(embed=embed)
    # ******************************************************************************************************************

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

        await message.channel.send(important_task_message(message.content, 2, user_dict[message.author.id], important_tasks))
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
    else:       # new
        await bot.process_commands(message)

keep_alive.keep_alive()

if __name__ == '__main__':
    import config
    bot.run(config.token)
