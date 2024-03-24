"""Initial version of all taskset generations"""

from XML_functions import save_xml, load_xml
from data_formats import Task
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

def scenarioGeneration(dependencies, WCETarray, deadlines, name):
    
    """generate, save tasks"""
    tasks = []
    for i in range(len(dependencies)):
        tasks.append(Task(i, WCETarray[i], deadlines[i], dependencies[i]))
    save_xml(tasks, name)
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
        for load in range(5, 11):
            if not os.path.isfile('Tasksets/' + app + '_' + str(float(load)/10) + '.xml'):
                [WCETArray, deadlineList] = WCETGen.constructWCETDistribution(int(s[0]), int(s[4]), s[5], s[6], s[7], int(s[8]), 
                                                                    float(load)/10,  s[9],  s[10])
                scenarioGeneration(DependencyList, WCETArray, deadlineList, app + '_' + str(float(load)/10))

    # Format: [num_tasks, range of resources, min max and mean wcet, range of critical tasks, min max and mean dependencies] x 1000 simulations
    synth = [4500, [2,5], [0.01, 30, 2], [200, 250], [1, 10, 5]]
    
    # For 960 iterations for validation of NXT Motion
    app = 'NXT Motion'
    s = taskset_hyperparameters[app].tolist()
    for iter in range(20):
        for processor in range(synth[1][0], synth[1][1]+1):
            for criticalTasks in range(synth[3][0], synth[3][1]+1, 5):
                if not os.path.isfile('Tasksets/' + app + '_' + str(iter) + '_' + str(processor) + '_' + str(criticalTasks) + '.xml'):
                    numDependencyArray = dependenceGenSynth.constructTaskDependencyDistribution(synth[0], synth[-1][-1]*synth[0], 
                                                                                synth[-1][0], synth[-1][1], synth[-1][-1], s[-1])
                    DependencyList = dependenceGenSynth.createDependenceLists(numDependencyArray)
                    deadline = 2 * synth[2][1] / s[5]
                    [WCETArray, deadlineList] = WCETGenSynth.constructWCETDistribution(synth[0], processor, deadline, synth[2][0], synth[2][1],
                                                                                synth[2][2], criticalTasks,  1,  0.5)
                    
                    scenarioGeneration(DependencyList, WCETArray, deadlineList, app + 
                                       '_' + str(iter) + '_' + str(processor) + '_' + str(criticalTasks))
                    
           
         
    return True
     
if __name__ == "__main__":
    main()