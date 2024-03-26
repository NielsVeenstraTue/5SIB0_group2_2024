from bs4 import BeautifulSoup as bs
import ast
from pprint import pprint
FILE = "5SIB0_group2_2024/Scheduler/dummy_1.xml"

#convert task to dict
def convert_to_dict(t)->dict:
    dep_str = t['dep']
    dep_list = ast.literal_eval(dep_str) if dep_str != "[]" else []
    return {'id':int(t['id']), 'e':float(t['e']), 'dl':float(t['dl']), 'dep':dep_list}

# return a list of idle processors
def processors_idle(time:float, schedule:list[list], n_proc:int)->list[int]:
    idle = []
    for i in range(n_proc):
        if (schedule[i] == []):
            idle.append(i)
        elif (schedule[i][-1]["time"] + schedule[i][-1]["e"] <= time):
            idle.append(i)
    return idle

# return next task with highest priority
def next_task_to_schedule(ready_list:list[dict])->dict:
    next_task = None
    if (ready_list != []):
        next_task = ready_list[0]
    for t in ready_list:
        if (t["dl"] < next_task["dl"]):
            next_task = t
    return next_task

def EDFschedule(file, n_processors:int):
    # Get the file as an input #############################
    with open(file, 'r') as f:
        data = f.read()

    task_set = bs(data, "xml")
    tasks = task_set.find_all('task')

    #create empty schedule
    schedule = []
    for i in range (n_processors):
        schedule.append([])

    #create list of dictionaries of task_set
    task_list_dict = []
    for t in tasks:
        task_dict = convert_to_dict(t)
        task_list_dict.append(task_dict)


    time = 0.0
    scheduled_tasks = 0
    nr_tasks = len(tasks)
    scheduled_ids = []

    # create list of tasks that have no dependencies before it (ready to schedule)
    ready_to_schedule = []
    for t in task_list_dict:
        if (t["dep"] == []): # first append all tasks which don't have a successor
                ready_to_schedule.append(t)
                task_list_dict.remove(t)

    while (scheduled_tasks < nr_tasks):
        time_list = []
        while (processors_idle(time, schedule, n_processors) != [] and next_task_to_schedule(ready_to_schedule) != None):
            for i in processors_idle(time,schedule, n_processors):
                next_task = next_task_to_schedule(ready_to_schedule)
                if (next_task != None):
                    next_task["time"] = time # add timestamp to the schedule
                    schedule[i].append(next_task) # add task to the schedule
                    time_list.append(next_task["e"] + time)
                    ready_to_schedule.remove(next_task)
                    scheduled_ids.append(next_task["id"])
                    scheduled_tasks += 1 # only increment when something is scheduled
        
        # increase time to smallest step
        time = min(time_list)

        #update ready_list
        task_list_dict_copy = task_list_dict.copy()
        for t in task_list_dict_copy:
            len_dep = len(t["dep"])
            dep_already_scheduled = 0
            for i in range(len_dep):
                if (t["dep"][i] in scheduled_ids):
                    dep_already_scheduled += 1
            if (dep_already_scheduled == len_dep):
                ready_to_schedule.append(t)
                task_list_dict.remove(t)

    pprint(schedule)

EDFschedule(FILE, 4)