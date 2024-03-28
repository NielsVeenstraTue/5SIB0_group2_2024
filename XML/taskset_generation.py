"""Initial version of all taskset generations"""

from XML_functions import save_xml, save_dep_xml
from data_formats import Task, Dependency
import dependenceGen
import WCETGen
import dependenceGenSynth
import WCETGenSynth
import random
import numpy as np
import pandas as pd
import os

# Set seed for reproducability
random.seed(0)
np.random.seed(0)

def create_load_excel(xlsx_loc):
    if os.path.isfile(xlsx_loc):
        df = pd.read_excel(xlsx_loc) 
    else:
        df = pd.DataFrame({'NXT Motion': [4301, 4095, 0, 22, 11, 1e-4, 1e-8, 2.25e-6, round(4301/18), 0.72, 0.3, 0.085],
                           'NXT Motion (specialized)': [4301, 4095, 0, 22, 11, 1e-4, 1e-8, 2.25e-6, round(4301/18), 0.72, 0.26, 0.085],
                           'Flexray': [14908, 26189, 0, 131, 14, 4.201e-3, 1e-9, 8.31e-5, 0, 1, 0, 0.01],
                           'Projection optics box (POB)': [1878, 1540, 0, 13, 6, 1e-4, 3.42e-8, 1.36e-6, round(1878/18), 0.7, 0.22, 0.135]},
                            index = ['Number of Tasks', 'Number of Dependencies', 'Dependency Minimum', 'Dependency Maximum',
                                    'Number of Resources', 'Period', 'WCET Minimum', 'WCET Maximum', 'Number of critical tasks',
                                    'Normal task deadline percentage', 'Critical task deadline percentage', 'alpha'])

        df.to_excel(xlsx_loc, index_label=df.columns.name)

    return df

def scenarioGeneration(fileLocation, dependencies, WCETarray, resources, deadlines):
    
    """generate, save tasks/ dependencies"""
    tasks = []
    for i in range(len(WCETarray)):
        tasks.append(Task(i, WCETarray[i], resources[i], deadlines[i]))
    save_xml(tasks, fileLocation + '/taskset.xml')
    
    deps = []
    for i in range(len(dependencies)):
        deps.append(Dependency(dependencies[i][0], dependencies[i][1]))
    save_dep_xml(deps, fileLocation + '/dependencies.xml')
    return True


def main():
      
    # Load real tasksets parameters
    applications = ['NXT Motion', 'NXT Motion (specialized)', 'Flexray', 'Projection optics box (POB)']
    
    # Generation tasksets with different loads on the processor (from 50% to 100% of their whole utilization)
    taskset_hyperparameters = create_load_excel('XML/taskset_parameters.xlsx')
    for app in applications:
        s = taskset_hyperparameters[app].tolist()
        numDependencyArray = dependenceGen.constructTaskDependencyDistribution(int(s[0]), int(s[1]), int(s[2]), int(s[3]), s[-1])
        DependencyList = dependenceGen.createDependenceLists(numDependencyArray)
        for load in range(50, 101):
            folder_loc = 'Tasksets/' + app + '_' + str(float(load)/100)
            if not os.path.exists(folder_loc):
                os.makedirs(folder_loc)
                [WCETArray, deadlineList, resourceList] = WCETGen.constructWCETDistribution(int(s[0]), int(s[4]), s[5], s[6], s[7], int(s[8]), 
                                                                    float(load)/100,  s[9],  s[10])
                scenarioGeneration(folder_loc, DependencyList, WCETArray, resourceList, deadlineList)

    # Format: [num_tasks, range of resources, min max and mean wcet, range of critical tasks, min max and mean dependencies] x 960 simulations
    synth = [4500, [2,5], [0.01, 30, 2], [200, 250], [1, 10, 5]]
    
    # For 960 iterations for validation of NXT Motion
    app = 'NXT Motion'
    s = taskset_hyperparameters[app].tolist()
    for iter in range(20):
        for processor in range(synth[1][0], synth[1][1]+1):
            for criticalTasks in range(synth[3][0], synth[3][1]+1, 5):
                folder_loc = 'Tasksets/' + app + '_' + str(iter) + '_' + str(processor) + '_' + str(criticalTasks)
                if not os.path.exists(folder_loc):
                    os.makedirs(folder_loc)
                    numDependencyArray = dependenceGenSynth.constructTaskDependencyDistribution(synth[0], synth[-1][-1]*synth[0], 
                                                                                synth[-1][0], synth[-1][1], synth[-1][-1], s[-1])
                    DependencyList = dependenceGenSynth.createDependenceLists(numDependencyArray)
                    deadline = 2 * synth[2][2] * synth[0] / processor
                    [WCETArray, deadlineList, resourceList] = WCETGenSynth.constructWCETDistribution(synth[0], processor, deadline, synth[2][0], synth[2][1],
                                                                                synth[2][2], criticalTasks,  1,  0.5)
                    
                    scenarioGeneration(folder_loc, DependencyList, WCETArray, resourceList, deadlineList)
                    
           
         
    return True
     
if __name__ == "__main__":
    main()