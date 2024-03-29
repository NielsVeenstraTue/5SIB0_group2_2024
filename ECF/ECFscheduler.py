from bs4 import BeautifulSoup as bs
import ast
import os
import cCALAP


def scheduler(tasks_list, successors, predecessors, ddt_dict, n_cores):
    
    schedule = list()
    scheduledTasks = {}
    enabledTasks = []
    gaps = [[] for _ in range(n_cores)]

    # Algorithm 2. Line 5
    for task in tasks_list:
        # If the task does not have a predecessor at all
        if task["id"] not in predecessors.keys(): enabledTasks.append(task)
        # If the task's predecessors are all scheduled
        elif all(x in scheduledTasks.keys() for x in predecessors[task["id"]]):
            enabledTasks.append(task)
    
    while len(scheduledTasks) != len(tasks_list):
        # Algorithm 2. Line 6
        min_id = None
        duedate_t = float('inf')
        for t in enabledTasks:
            value = float(ddt_dict.get(str(t['id'])))
            if value is not None and value < duedate_t:
                # Get task ID and duedate
                min_id = t['id']
                duedate_t = value

        # scheduling task
        task_sched = tasks_list[int(min_id)]
        # Get task resource
        resource = int(task_sched["r"])
        # Get task execution time
        wcet = float(task_sched["e"])
        # Get task deadline
        deadline = float(task_sched["d"])
        
        # Algorithm 2. Line 7
        c_last_pred_t = 0
        # If task has a predecessor pass
        if min_id in predecessors.keys():
            for pred_task in predecessors[min_id]:
                info = scheduledTasks[pred_task]
                c_last_pred_t = max(c_last_pred_t, float(info["c"]))       
        
        # Algorithm 2. Line 8
        if len(gaps[resource]) != 0:
            min_gap_idx = len(gaps[resource])-1
            wentInsideIfCondition = False
            for gap_idx in range(len(gaps[resource])):
                if max(c_last_pred_t, gaps[resource][gap_idx][0]) + wcet <= gaps[resource][gap_idx][1] and min_gap_idx < gap_idx:
                    min_gap_idx = gap_idx
                    wentInsideIfCondition = True
            if not wentInsideIfCondition:
                min_gap_idx = None
        else:
            min_gap_idx = None

        # Algorithm 2. Lines 9-15
        if min_gap_idx != None:
            starting_time = max(c_last_pred_t, gaps[resource][min_gap_idx][0])
        else:
            # Find completion time of last task in resource r
            last_completion_time = 0
            for task in scheduledTasks.keys():
                task = scheduledTasks[task]
                if int(task["r"]) == resource:
                    last_completion_time = max(last_completion_time, float(task["c"]))
            starting_time = max(c_last_pred_t, last_completion_time)

        # Algorithm 2. Lines 16-22
        completion_time = starting_time + wcet
        if completion_time > duedate_t:
            return None
        else:
            # Need to create new gaps
            # If there was a gap
            if min_gap_idx != None:
                if starting_time == gaps[resource][min_gap_idx][0]:
                    # If the starting times and finish time for gap and task are the same
                    if completion_time == gaps[resource][min_gap_idx][1]:
                        gaps[resource].pop(min_gap_idx)
                    # If it leaves a gap in the end
                    else:
                        gaps[resource][min_gap_idx][0] = completion_time
                else:
                    # If it leaves a gap in the beginning
                    if completion_time == gaps[resource][min_gap_idx][1]:
                        gaps[resource][min_gap_idx][1] = completion_time
                    # If it leaves two gaps in the corners
                    else:
                        gaps[resource].insert(min_gap_idx+1, [completion_time, gaps[resource][min_gap_idx][1]])
                        gaps[resource][min_gap_idx][1] = starting_time
            else:
                if last_completion_time < starting_time:
                    gaps[resource].append([last_completion_time, starting_time])
                    
            # Update schedule and scheduled tasks
            schedule.append({"id":min_id, "e": wcet, "r": resource, "d": deadline, "s": starting_time, "c": completion_time})
            scheduledTasks[min_id] = {"id":min_id, "e": wcet, "r": resource, "d": deadline, "s": starting_time, "c": completion_time}
            # Update enabled tasks
            if min_id in successors.keys():
                for task in successors[min_id]:
                    if all(x in scheduledTasks.keys() for x in predecessors[task]):
                        enabledTasks.append(tasks_list[int(task)])
            enabledTasks.remove(tasks_list[int(min_id)])

    return schedule       
            
def ECF(taskset, dependencies):
    taskset, successors, numResources, CALAPvals = cCALAP.CALAPCalculation(taskset, dependencies)
    deps = cCALAP.dep2list(dependencies)
    predecessors = cCALAP.convertDep2Pred(deps)
    schedule = scheduler(taskset, successors, predecessors, CALAPvals, numResources)
    return schedule

#T_xml = os.getcwd() + r"\ECF\dummy_1.xml"
#D_xml = os.getcwd() + r"\ECF\Dependencies.xml"
#print(ECF(T_xml, D_xml))