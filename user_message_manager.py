import random

def help_command_message():
    """ This function returns the bot message when the user makes a 'help' request. """

    bot_help_msg = ("I support the following commands:\n" 
            "\n:one: " + "add a task by typing \"**remind me to \'task\' at \'time\'**\n" +
            "\n:two: " + "delete a task by typing \"**delete task_ID**\"\n" +
            "\n:three: " + "edit a task by typing \"**edit task_ID : new_task task_time**\" for example \"edit 1 : drink chamomile and read at 8:00 pm\"\n" +
            "\n:four: " + "check all tasks you completed by typing \"**completed**\"\n" +
            "\n:five: " + "view all tasks you scheduled and completed by typing \"**view**\"\n" +
            "\n:six: " + "complete a task by typing \"**completed task task_ID**\"\n" +
            "\n:seven: " + "mark a task as important by typing \"**mark task task_ID as important**\"\n" +
            "\n:eight: " + "mark a task as not important anymore by typing \"**mark task task_ID as not important**\"\n" +
            "\n:nine: " + "clear your schedule by typing \"**clear all**\"\n")
    return bot_help_msg

def examples_command_message():
    """ This function returns the bot message when the user makes an 'examples' request. """

    bot_examples_msg = (
            "\nadding a task " + ":arrow_right:" + " remind me to sleep at 10:00 pm\n" +
            "\ndeleting a task " + ":arrow_right:" + " delete 1\n" +
            "\nediting a task " + ":arrow_right:" + " edit 1 : remind me to sleep at 9 pm\n" +
            "\nmarking a task as completed " + ":arrow_right:" + " completed 1\n" +
            "\nviewing all scheduled and completed tasks " + ":arrow_right:" + " view\n"
    )
    return bot_examples_msg

def tips_command_message():
    """ This function returns the bot message when the user enters a 'tips' request. """

    bot_tips_msg = (
        "\n:bulb: " + "you can get any task_ID by typing \"**view**\"\n" +
        "\n:bulb: " + "you can change the mood by typing \"**change mood**\"\n" +
        "\n:bulb: " + "if you have a task marked as important and you want to remove that tag, simply type \"**mark task task_ID as not important**\"\n" +
        "\n:bulb: " + "you can see examples of the commands I support by typing \"**examples**\"\n" +
        "\n:bulb: " + "whenever you are stuck using a command, type \"**help**\"\n"
    )
    return bot_tips_msg

def get_task_ID_from_edit_msg(message_content):
    """ Input: message_content = message.content, a discord-specific function.
        Output: the task_ID entered by the user. """

    task_ID = ''
    user_msg = message_content
    splited_sentence = user_msg.split()  # split the user message into a list
    if splited_sentence[0].lower() in ["edit", "!edit"]:
        task_ID = splited_sentence[1]  # get the task_ID of the task-to-edit

    return task_ID



def important_task_message(message_content, task_ID_index, toDos_dictionary, important_tasks_dictionary):
    """ Input:
            -> message_content = message.content, the actual message of the user
            -> task_ID_index = an int referencing the index of the task_ID in the user message
            -> target_dictionary = the dictionary associated with the "not important" task
        Output: Returns a bot_message which tells the user if their action successfully marked a task as "important,"
            or warns the user if their message is wrongly formatted. """

    bot_msg = 'Something went wrong. Type Help.'
    splited_sentence = message_content.split()              # split the user message into a list

    if splited_sentence[task_ID_index].isdigit():
        task_ID = int(splited_sentence[task_ID_index])
        if task_ID not in toDos_dictionary.keys():          # if task_ID not in toDos then edit no task and warn user
            bot_msg = f'no task is associated with the ID {task_ID}    :dizzy_face:'
            return bot_msg
        else:
            # store the important task in important dictionary:
            task_details = toDos_dictionary[task_ID][0]
            task_time = toDos_dictionary[task_ID][1]
            important_task_msg = task_details + ' at ' + task_time
            important_tasks_dictionary[task_ID] = important_task_msg
            bot_msg = 'task ' + str(task_ID) + ' has been marked as important.'

    return bot_msg

def not_important_task_message(message_content, task_ID_index, target_dictionary):
    """ Input:
            -> message_content = message.content, the actual message of the user
            -> task_ID_index = an int referencing the index of the task_ID in the user message
            -> target_dictionary = the dictionary associated with the "not important" task
        Output: Returns a bot_message which tells the user if their action successfully marked a task as "not important,"
            or warns the user if their message is wrongly formatted """

    bot_msg = 'Something went wrong. Type Help.'
    splited_sentence = message_content.split()          # split the user message into a list

    if splited_sentence[task_ID_index].isdigit():
        task_ID = int(splited_sentence[task_ID_index])
        if task_ID not in target_dictionary.keys():     # if task_ID not in toDos then edit no task and warn user
            bot_msg = f'no task is associated with the ID {task_ID}    :dizzy_face:'
            return bot_msg
        else:
            target_dictionary.pop(task_ID)
            bot_msg = 'task ' + str(task_ID) + ' has been removed from important tasks'

    return bot_msg

def view_important_tasks(important_tasks_dictionary):

    bot_msg = ''

    if (not important_tasks_dictionary):
        bot_msg = 'There are no tasks marked as important. To mark a task as important, type \"**mark task task_ID as important**\"'
    else:
        for id in important_tasks_dictionary:
            bot_msg += '➼ ID:' + str(id) + '| :red_circle: ' + important_tasks_dictionary[id] + '\n'
            print('the important tasks dic:')
            print(important_tasks_dictionary)

    return bot_msg

def table_view_important_tasks():
    return

def edit_important_tasks(task_ID, new_task, new_time, target_dictionary):
    if task_ID in target_dictionary:
        target_dictionary[task_ID] = new_task + new_time
    print(target_dictionary)

def bot_greeting_msg():
    """ This function returns the bot message when the user enters a greeting message. With a random probability of a
        1/6, the bot also awares the user that they can request 'tips', get 'examples', ask for 'help', or see the 'user
        manual' to allow new users to learn how to use the bot. """

    bot_greetings = ['Hi', 'Hya', 'Hello', 'Hey']               # possible bot replies
    bot_response = ''
    random_number = random.randint(1, 4)
    tips_msg = "\ntry typing \"tips\""
    examples_msg = "\ntry typing \"examples\""
    help_msg = "\ndon't shy away from asking for help, just type \"help\""
    user_manual_msg = "! You can check the user manual by visiting :globe_with_meridians:: https://github.com/xlab-classes/cse442-spring2022-team-terms-co"

    if (random_number == 1):
        bot_response = random.choice(bot_greetings) + tips_msg
    elif (random_number == 2):
        bot_response = random.choice(bot_greetings) + examples_msg
    elif (random_number == 3):
        bot_response = random.choice(bot_greetings) + help_msg
    elif (random_number == 4):
        bot_response = random.choice(bot_greetings) + user_manual_msg

    return bot_response