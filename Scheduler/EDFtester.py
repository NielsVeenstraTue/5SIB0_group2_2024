import EDFscheduler
import os
import time
import pandas as pd

def write_list(a_list, write_loc):
    file = open(write_loc,'w')
    for item in a_list:
        file.write(str(item)+"\n")
    file.close()

def main():
    ## Select one of the following i:
    # i=0   #For Vasilis
    # i=1   #For Daniil
    # i=2   #For Corniels
    # i=3   #For Niels    
    data_directory = os.getcwd() + r"\Tasksets"
    counter = 0
    total_files = 0
    if os.path.exists(os.path.join(data_directory, "EDF_results_" + str(i+1) + ".csv")):
        df = pd.read_csv(os.path.join(data_directory, "EDF_results_" + str(i+1) + ".csv"))
    else:
        df= pd.DataFrame({"name": [], "schedulable": [], "time":[]})
        df.to_csv(os.path.join(data_directory, "EDF_results_" + str(i+1) + ".csv"), index=False)
    
    folder_list = []
    for subdir, dirs, files in os.walk(data_directory):
        folder_list.append(subdir)
    file_loc = ["taskset.xml", "dependencies.xml"]
    for subdir in folder_list[i*271:(i+1)*271]:
    # for subdir in folder_list[1:-1]:
        name = os.path.basename(os.path.normpath(subdir))
        if name == "Tasksets": continue
        print(name)
        if not df.isin([name]).any().any():
            total_files +=1
            start = time.time()
            schedule = EDFscheduler.EDF(os.path.join(subdir, file_loc[0]), os.path.join(subdir, file_loc[1])) # 0: taskset, 1: dependencies
            end = time.time()
            temp = {"name": [name], "schedulable": [not(not(schedule))], 'time':[end-start]}
            df_temp = pd.DataFrame(temp)
            df_temp.to_csv(os.path.join(data_directory, "EDF_results_" + str(i+1) + ".csv"), mode='a', index=False, header=False)
            df = pd.concat([df, df_temp], ignore_index=True)
            if schedule != None: counter +=1
        
    return float(counter), float(total_files)

if __name__ == "__main__":
    schedules, inTotal = main()
    print("Schedulability performance: ", schedules/inTotal*100, "%")
    