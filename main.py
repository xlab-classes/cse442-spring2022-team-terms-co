from sched import scheduler
from winreg import QueryReflectionKey

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
 

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

#Read the private key from a local file
TOKEN = 'OTQ1ODc3NjkyNjczMzE4OTYz.YhWjPw.Ze7bJVKShOhzpbNj20ReINg9Pso'
toDos = {0: 0, -1: ''}
completed = {}
pending_task = {}#tasks that time have passed but havent been completed
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
# scheduler = BackgroundScheduler()
# scheduler.start()
async def func(msg, task_details, task_time):
    """
    A function to be added to the scheduler when a job is added. This function sends an embed message notifying the
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
        color=0xEABBC2)#0x6A5ACD
    #await c.send(embed=embed)
    await msg.channel.send(embed=embed)

#create a func to delete message
#call it in delete and clear all
def delete(id):
    scheduler.remove_job(id)
    scheduler.print_jobs()

# def pending(id):
    
#     taskID = id
#     task=  toDos[taskID][0]

#     completed_task = toDos.pop(taskID)
#     pending_task[taskID] = completed_task
#     print(pending)
 
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
  
# Snigdha's code:********************************************************************************************************
    #add task
    regexCheck = re.match(".*(?![remind me to]).+", message.content)
    remindMeCheck = re.match("(.*(?=[R-r]emind me to).*)", message.content)
    if bool(regexCheck) and remindMeCheck:
      if ' at' in message.content:
        split_index = message.content.find(' at')
        #print(split_index)
        tim_e = message.content[split_index + 3:].replace(' ','')
        #print(tim_e)
        #.*([0-9]\s?[AM|am|PM|pm]+)
        # time format to handle 5 : 15am
        matched = re.match(".*([0-9]\s?[AM|am|PM|pm]+)", tim_e)
        #print(matched)
        is_match = bool(matched)
        if not is_match:
            embed = discord.Embed(
                title ="Unable to add the task. To add a task send a message in the following format:",
                description = 'remind me to do a task at time\n \n ex:\n remind me to cook dinner at 5:30pm',
            color =0xeb34c9
            )
            await message.channel.send(embed=embed)
            return 
            # await message.channel.send(
            #     "Invalid format. Send a message 'help' for assistance with valid formats."
            # )
            # return
        taskID = toDos[0] + 1
        toDos[0] = taskID
        toDos[-1] = message.content[12:split_index]
        #print(toDos)
        #print(taskID, " task ID")
        toDos[taskID] = (message.content[13:split_index].strip(), tim_e)
        print(toDos)
        await message.channel.send(replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID))
    # Rami's Addition:------------------------------------------------------------------------------------------
        print('channel: ' + str(message.channel))
        user_time = process_input_time(tim_e)

        military_time = time_to_military(user_time)
        time_hrs = military_time[0] + military_time[1]
        time_mins = military_time[3] + military_time[4]
        task_details = toDos[taskID][0]
        scheduler.add_job(func, CronTrigger(hour=time_hrs, minute=time_mins, second="0"),(message, task_details, military_time,), id=str(taskID), replace_existing=True)
        scheduler.print_jobs()
          
     # ----------------------------------------------------------------------------------------------------------    
        return
      else:
        split_index = message.content.find(' to')
        task = message.content[split_index + 3:].replace(' ','').strip()
        toDos[-1] = task
        print(toDos)
        await message.channel.send(
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
      await message.channel.send(replies[random.randrange(len(replies))] + ". The task ID is " + str(taskID))
      return
        
#***********************************************************************************************************************

# Tanvie's code:********************************************************************************************************
    # delete task
    elif message.content.startswith('delete '):
        split_index = 7
        #print(split_index)
        to_del = message.content[split_index:]
        #the task ID to delete is to_del
        print(to_del)
        if not to_del.isdigit():
            embed = discord.Embed(
                title ="Unable to delete the task. To delete a task send it in the format below:",
                description = 'delete task_ID\n \n ex:\n delete 4',
            color =0xeb34c9
            )
            await message.channel.send(embed=embed)
            # await message.channel.send("Invalid format. Send a message 'help' for assistance with valid formats.")
        elif int(to_del) in toDos:
            toDos.pop(int(to_del.strip()))
            delete(to_del)
            await message.channel.send("You have successfully deleted a task!")
        elif int(to_del) in completed:
            completed.pop(int(to_del.strip()))
            await message.channel.send("You have successfully deleted a completed task!")
        else:
            embed = discord.Embed(
                title ="Unable to delete the task. To delete a task send it in the format below:",
                description = 'delete task_ID\n \n ex:\n delete 4',
            color =0xeb34c9
            )     
            await message.channel.send(embed=embed)          
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
        
        embed = discord.Embed(
            title ="Task id not found. To complete a task send it in the format below:",
            description = "Completed task task_ID\n \n"+'ex:\n Completed task 4',
        color =0x4e03fc
        )
        await message.channel.send(embed=embed) 
        return         
        # await message.channel.send("You did not correctly list a task, please call help to see the correct formatting")
      else:
        m = "Congrats on completing task: " + str(message_id)
        completed_task = toDos.pop(message_id)
        completed[message_id] = completed_task
        print(completed)
        delete(str(message_id))
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
        await message.channel.send(embed=embed)

#***********************************************************************************************************************
# Elijah's code:********************************************************************************************************
    #clear all
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
                    
                # await message.channel.send('Your edit message is not formatted correctly. Type help.    :eyes:')
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
    # else:
    #     await message.channel.send(
    #         "Invalid format. Send a message 'help' for assistance with valid formats."
    #     )

keep_alive.keep_alive()
client.run(TOKEN)
