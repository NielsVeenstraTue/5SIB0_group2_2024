import random
import numpy as np

def constructTaskDependencyDistribution(numOfTasks, numOfDependencies, minDependence, maxDependence, meanDependence, alpha):

    # Generate # of dependences based on the Beta Distribution
    
    # Generate random values within the range [minDependence, maxDependence]
    array = maxDependence * np.random.beta(alpha, alpha*(maxDependence - meanDependence)/(meanDependence - minDependence), numOfTasks)
    # Round from float to int and convert from array to list
    array = list((np.round(array)).astype(np.int32))
    
    # Check if total sum of generated values are equal to numOfDependencies
    array = fixTotalDependences(array, numOfDependencies, minDependence, maxDependence)
    # Check if first maxDependence indices do not have dependences larger than their index
    array = fixFirstDependences(array, maxDependence)
    
    return array


def fixTotalDependences(sequence, desiredSum, minValue, maxValue):
    # Calculate the current sum of the array
    currentSum = sum(sequence)

    # Adjust one of the elements to make the sum equal to the desired sum
    difference = desiredSum - currentSum

    while(difference != 0):
        task_idx = random.randint(0, len(sequence) - 1)
        if (difference > 0):
            if sequence[task_idx] == maxValue:
                continue
            sequence[task_idx] += 1
            difference -=1
        else:
            if sequence[task_idx] == minValue:
                continue
            sequence[task_idx] -= 1
            difference +=1     
    
    return sequence     
    
    
def fixFirstDependences(sequence, maxValue):
    
    for i in range(maxValue):
        swap_val = sequence[i]
        if swap_val > i:
            task_idx = sequence.index(i , i, len(sequence) - 1)
            sequence[i] = sequence[task_idx]
            sequence[task_idx] = swap_val
            
    return sequence

def createDependenceLists(sequence):
    
    rng = np.random.default_rng()
    dependenceList = list()
    for i in range(len(sequence)):
        if sequence[i] == 0:
            dependenceList.append([])
        else:
            np.random.seed(i)
            rand_dep = rng.choice(i, size=sequence[i], replace=False).tolist()
            dependenceList.append(sorted(rand_dep))
    return dependenceList
