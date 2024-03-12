import random
import numpy as np

# Set seed for reproducability
random.seed(0)
np.random.seed(0)


def constructTaskDependencyDistribution(numOfTasks, numOfDependencies, minDependence, maxDependence):

    # Generate # of dependences based on the Beta Distribution
    # Alpha parameter chosen arbitrarily so that we at least have one 22-dependence occurence
    alpha = 0.085
    # Arbirtrary mean of distribution based on the number of tasks and total dependences
    desMean = numOfDependencies/numOfTasks
    # Generate random values within the range [0, 22]
    array = maxDependence * np.random.beta(alpha, alpha*(maxDependence - desMean)/(desMean - minDependence), numOfTasks)
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


# For the example of NXT Motion
num_tasks = 4301
num_dependences = 4095
min_dependence = 0
max_dependence = 22
array = constructTaskDependencyDistribution(num_tasks, num_dependences, min_dependence, max_dependence)

print(f"First {max_dependence} values of the array: {array[:max_dependence]}")
print("Sum of the array:", sum(array))
print("Max of the array:", max(array))
print("Min of the array:", min(array))
print("Occurences in array:", [array.count(i) for i in range(max(array)+1)])
