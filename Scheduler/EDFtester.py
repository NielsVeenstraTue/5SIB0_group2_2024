import EDFscheduler
import os
import time

def write_list(a_list, write_loc):
    file = open(write_loc,'w')
    for item in a_list:
        file.write(str(item)+"\n")
    file.close()

def main():
    data_directory = os.getcwd() + r"\Tasksets"
    counter = 0
    total_files = 0
    for subdir, dirs, files in os.walk(data_directory):
        total_files +=1
        print(subdir)
        file_loc = []
        for file in files:
            file_loc.append(os.path.join(subdir, file))
        if len(file_loc) == 2:
            start = time.time()
            schedule = EDFscheduler.EDF(file_loc[1], file_loc[0]) # 1: taskset, 0: dependencies
            end = time.time()
            write_list([str(not(not schedule)), end - start], subdir + r'\output.txt')
            if schedule != None: counter +=1
        
    return float(counter), float(total_files)

if __name__ == "__main__":
    schedules, inTotal = main()
    print("Schedulability performance: ", schedules/inTotal*100, "%")
    