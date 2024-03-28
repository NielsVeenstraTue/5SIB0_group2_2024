from bs4 import BeautifulSoup as bs
import ast
import os
from cDDPR import xml2list, splitTasksPerResource, convertDep2dict

FILE = "5SIB0_group2_2024/Scheduler/dummy_xml_inputs/dummy_1.xml"



# def schedule(file):
    
#     # Get the file as an input #############################
#     with open(file, 'r') as f:
#         data = f.read()
    
#     task_set = bs(data, "xml")
    
#     tasks = task_set.find_all('task')
#     #print(tasks)
    
#     #########################################################
#     # Computing due date per resource #######################
    
#     wcet = [] # List to hold all the 'e' values of all the tasks. Can be indexed by ID.
    
#     for id, task in enumerate(tasks):
#         succ = {}
#         d_t = task['dl']
        
#         for t in tasks:
#             dep_str = t['dep']
#             dep_list = ast.literal_eval(dep_str) if dep_str != "[]" else []
            
#             if len(wcet) < len(tasks):
#                 wcet.append(float(t['e'])) 
            
#             if id in dep_list: 
#                 succ[t['id']] = t['dl']
        
#         succ_ordered = dict(sorted(succ.items(), key=lambda item: item[1], reverse=True))
#         #print(succ_ordered)
        
#         dd_t = float('inf')
        
#         for t_prime_id, dd_t_prime in succ_ordered.items():
#             if float(dd_t_prime) <= dd_t:
#                 dd_t = float(dd_t_prime) - wcet[int(t_prime_id)]
#             else:
#                 dd_t = float(dd_t) - wcet[int(t_prime_id)]
        
#         dd_t = min(dd_t, float(d_t))
#         #succ_dd_t.append(dd_t)
#         task['dd'] = str(dd_t)
        
 
#     #######################################################
#     # Scheduling ##########################################
    
#     ST = []
#     ET = tasks
    
#     while len(ST) != len(tasks):
#         ET = []
    
    
    
#     print(tasks)
    
    


# schedule(FILE)

DD_DICT_DUMMY = {
    "0": 1,
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "6": 7
}

T_xml = os.getcwd() + r"\VasilisImplementation\dummy_1.xml"
D_xml = os.getcwd() + r"\VasilisImplementation\Dependencies.xml"

#T_xml = "5SIB0_group2_2024/VasilisImplementation/dummy_1.xml"
#D_xml = "C:/Users/Asus ZenBook/OneDrive/Рабочий стол/EDA/5SIB0_group2_2024/VasilisImplementation/Dependencies.xml"

t_xml = xml2list(T_xml)
d_xml = xml2list(D_xml)
d_dict = convertDep2dict(d_xml)

#t_p_r, d_p_r = splitTasksPerResource(t_xml, d_xml, 2)

#print(d_dict)


# Algorithm 2 Implementation
def scheduler(tasks_list, dep_dict, ddt_dict, n_cores):
    
    S = {}
    ST = ['0']
    ET = []
    i = 0
    gaps = []

    
    while len(ST) != len(tasks_list):
    
        # Algorithm 2. Line 5
        if (len(ST) != 0):
            for key, value in dep_dict.items():
                if key in ST:
                    for element in value:
                        for task in tasks_list:
                            if task['id'] == element:
                                ET.append(task)
                            else: continue
        else:
            ET = tasks_list
        

        # Algorithm 2. Line 6

        min_id = None
        min_value = float('inf')

        for t in ET:
            value = ddt_dict.get(t['id'])
            if value is not None and value < min_value:
                min_id = t['id']
                min_value = value
            
        
        # Algorithm 2. Line 7
        
        c_last_pred_t = 0

        if (i):
            pred_t_c_t_prime = []
            for key, value in dep_dict.items():
                if min_id in value:
                    for k, v in S.items():
                        if k == key:
                            pred_t_c_t_prime.append(k['end'])
            
            c_last_pred_t = max(pred_t_c_t_prime)
        else:
            c_last_pred_t = 0

        # Algorithm 2. Line 8
        if gaps != []:
            g_chosen = pass # TODO: Implement gaps. Should look like [[start,end],[start,end]]
        else:
            g_chosen = []

        # Algorithm 2. Lines 9-15
        if g_chosen != None or g_chosen == []:
            s_t = max(c_last_pred_t, g_chosen[0])
        else:
            for task in ET:
                if task["id"] == min_id:
                    tasks_for_resource = S[task['r']]
                    end_values = [S["end"] for t in tasks_for_resource.values()]
                    max_end_value = max(end_values)


            c_last_r = max_end_value #TODO: Implement last completion time of resource 
            s_t = max(c_last_pred_t, c_last_r)

        
        # Algorithm 2. Lines 16-22
        for t in ET:
            if t['id'] == min_id:
                e_t = t['e']
            
        c_t = s_t + e_t

        for id, value_ddt in ddt_dict:
            if id == min_id:
                dd_t = value_ddt
        
        if c_t > dd_t:
            return 'Deadline miss. Task set unschedulable by this algorithm.'
        else:
            # Algorithm 2. Line 20-22
            for task in ET:
                if task['id'] == min_id:
                    S[task['r']][task['id']]['start'] = s_t
                    S[task['r']][task['id']]['end'] = c_t
                    S[task['r']][task['id']]['deadline'] = dd_t
                    ST.append(task)
                    ET.remove(task)

                    for i in range(n_cores):
                        gaps.append([])

                    if c_t < dd_t:
                        gaps[int(task['r'])].append([s_t, c_t])
            


        # Keeping track of loop iterations
        i += 0

    # Returning the ready schedule
    return S

schedule = scheduler(t_xml, d_dict, DD_DICT_DUMMY)

print(schedule)

