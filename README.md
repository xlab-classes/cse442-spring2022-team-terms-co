# CSE442 Project
### https://www-student.cse.buffalo.edu/CSE442-542/2022-Spring/cse-442s/cse442-spring2022-team-terms-co/static/

# **About**
TaskBot is a Discord bot that can be used to schedule daily tasks. TaskBot offers many functionalities to help in scheduling tasks. Whenever you schedule a task, TaskBot will associate a task_ID with that task. You can retrieve the task_ID of the tasks you scheduled by typing *view*. Knowing the task_ID will help you do many things with your tasks, like deleting or editing them. While using the commands may seem intmidating at first, it is easy to get used to them quickly. Moreover, TaskBot is designed to handle users messages sent in the worng format by notifying them of possible errors they made. We hope to make the lives of our users easier with the convenience of our very own toDoBot!
<br/>
<br/>
![image](https://user-images.githubusercontent.com/43181965/161441175-a41d4a3d-bfd9-4864-b452-45843af50e18.png)
<br/>
# **Using the Bot**
You can invite TaskBot to your server by following the instructions on https://www-student.cse.buffalo.edu/CSE442-542/2022-Spring/cse-442s/cse442-spring2022-team-terms-co/static/. Once TaskBot has been invited, you can try greeting it by typing *Hey*, *Hi*, or *Hello* and it will reply back and *sometimes* offer you some of the keywords the will help you use its functionality! 

# **Getting Help**
To simplify using the bot for new users, we have included some commands that the user can enter to help them see the functionalities that the bot support.

|    Feature    |    Command    |                           Description                              |
| ------------- | ------------- | ------------------------------------------------------------------ |             
| Help          |  *help*       | This command can be used whenever the user is stuck using TaskBot  |          
| Tips          |  *tips*       | Allows the user to see some tips of how to use TaskBot             |            
| Examples      |  *examples*   | Shows some examples of the commands supported by TaskBot           |       

# **Features**

|           Feature          |                        Command                            |         
| -------------------------- | --------------------------------------------------------- |              
| Adding a Task              |  *remind me to task_description at desired_time*          |      
| Editing a Task             |  *edit task task_ID : new_task_details at new_task_time*  |              
| Deleting a Task            |  *delete task_ID*                                         |     
| Viewing Scheduled Task     |  *view*                                                   |
| Marking Tasks as Important |  *mark task task_ID as important*                         |
| Removing the Important Tag |  *mark task task_ID as not important*                     |
| Marking Tasks as Completed |  *Completed task task_ID*                                 |
| List Important Tasks Only  |  *list important tasks*                                   |


# **TaskBot Mood**

You can control the mood of message reminders sent by TaskBot. [In Progress...]
<img src="https://github.com/favicon.ico" width="48">

# **A Walkthrough**
Let's try using TaskBot to schedule our tasks. We will start by adding our first task by sending the bot the following message: *remind me to submit my homework at 
11:00am*. The bot will reply with:
<br/>
<br/>
<img src = "https://user-images.githubusercontent.com/43181965/161452607-29550cdb-6700-471b-b938-f8972e579344.png">
<br/>
<br/>  
Now, let us mark that task as important by typing *mark task 1 as important*. The bot's reply is:
<br/>
<br/>
<img src = "https://user-images.githubusercontent.com/43181965/161452643-507438b5-3c62-471d-907f-4bf556b1f4fa.png">
<br/>
<br/>
Upon typing *view*, we can see our schedule so far:
<br/>
<br/>
<img src = "https://user-images.githubusercontent.com/43181965/161452660-c97bca8e-b178-40a2-bb4f-f6dccbbc8b7b.png">
<br/>
<br/>
  
Suppose we want to edit the task we just scheduled and wish to change its time. We simply type: *edit task 1 : submit my homework at 11:59 am*. The bot will reply with:
<br/><br/>
![image](https://user-images.githubusercontent.com/43181965/161452737-77efbf6b-8806-4302-8f44-afad4fb29b7a.png)
<br/><br/>
The changes will be reflected on the schedule:
<br/><br/>
![image](https://user-images.githubusercontent.com/43181965/161452758-a5367872-76df-4b9a-9751-08b533b7256f.png)
<br/><br/>
Now, we can mark our task as completed by typing *completed task 1*:
<br/><br/>
![image](https://user-images.githubusercontent.com/43181965/161452804-fb1c555e-691b-41e1-adea-618b3092d764.png)
<br/><br/>
Finally, we can delete the task we just completed and make sure that our schedule is totally empty:
<br/><br/>
![image](https://user-images.githubusercontent.com/43181965/161452854-388715d1-b883-4990-8c9a-89582cb6b264.png)
<br/>


 *  *  *  *  *  *   *  *  *  *  *  *   *  *  *  *  *  *   *  *  *  *  *  *  
# **Links**
cse442-spring2022-team-terms-co created by GitHub Classroom

https://app.zenhub.com/workspaces/termsco-62041763e03d170016443702/board?invite=true

Discord:
https://discord.gg/WrPZKdEvma

Wireframe:
https://www.figma.com/file/S9JxKlzKobq5OIIHJ46Gp8/TERMS%26Co-Wireframe

ZenHub
https://app.zenhub.com/workspaces/termsco-62041763e03d170016443702/board?repos=457501643,459349236

 *  *  *  *  *  *   *  *  *  *  *  *   *  *  *  *  *  *   *  *  *  *  *  *  
