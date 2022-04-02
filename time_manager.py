from datetime import datetime
import pytz

def process_input_time(input_time):
    """
        This function is to be called before converting the user input time to military time, because a user input time
        may not match the military time conversion function.
    """

    # step 1: Get the hours from the user input
    if input_time[0].isdigit() and input_time[1].isdigit():
        time_hrs = input_time[0] + input_time[1]

    else:
        time_hrs = input_time[0]
    pm_flag = False
    am_flag = False

    # Step 2: Get the minutes from the user input - There are 4 cases that we must handle
    time_mins = '00'  # initialize a variable to store the minutes

    if len(input_time) == 7:  # case 1: proper format - double digit hours [10:00pm, 11:45 am, etc...]
        time_mins = input_time[3] + input_time[4]
        if input_time[5] == 'p' or input_time[5] == 'P':
            pm_flag = True
        else:
            am_flag = True

    elif len(input_time) == 6:  # case 2: proper format - single digit hours [1:28 am, 5:03 PM,etc...]
        time_mins = input_time[2] + input_time[3]
        if input_time[4] == 'p' or input_time[4] == 'P':
            pm_flag = True
        else:
            am_flag = True

    elif len(input_time) == 4:  # case 3: improper format - double digit hours [12pm, 12am, 10pm, 11am, etc...]
        time_mins = '00'  # augment 0s for minutes
        if input_time[2] == 'p' or input_time[2] == 'P':
            pm_flag = True
        else:
            am_flag = True

    elif len(input_time) == 3:  # case 4: improper format - single digit hours [1pm, 5am, 9pm, etc...]
        time_mins = '00'  # augment 0s for minutes
        if input_time[1] == 'p' or input_time[1] == 'P':
            pm_flag = True
        else:
            am_flag = True

    user_input = time_hrs + ':' + time_mins

    if pm_flag: user_input = user_input + ' ' + 'PM'
    if am_flag: user_input = user_input + ' ' + 'AM'
    print("enter the function: " + user_input)
    print('pm_flag: ' + str(pm_flag))
    print(am_flag)
    return user_input

def time_to_military(t):
    """
    A function to convert a time, t, to a military time. t should be formatted correctly.
    That is, t can be of the following two forms:
    hours:minutes AM, or
    hours:minutes PM.
    """
    # my_datetime = datetime(2023, 2, 13, 17, 10, 27, tzinfo = pytz.utc)

    # military_time = datetime(t, '%I:%M %p').strftime('%H:%M')
    # my_datetime_est = military_time.astimezone(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    # print(my_datetime_est)
    # return my_datetime_est
    # timezone = pytz.timezone('America/New_York')
    # military_time = datetime.utcnow().astimezone(tz=timezone)
    
    military_time = datetime.strptime(t, '%I:%M %p').strftime('%H:%M')
    print(military_time)
    return military_time

