import os
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from scipy import stats

def main():
   
    data_directory = os.getcwd() + r"\Tasksets"
    ECF_data_loc = os.path.join(data_directory, "ECF_results.csv")
    EDDF_data_loc = os.path.join(data_directory, "EDDF_results.csv")
    dfECF = pd.read_csv(ECF_data_loc)
    dfEDDF = pd.read_csv(EDDF_data_loc)
    
    name_list = list()
    industrial_name_list = [[] for _ in range(4)]
    for ind in dfECF.index:
        name = dfECF["name"][ind]
        if name[:11] == "NXT Motion_":
            if name[12] != "." : name_list.append(ind)
            else: industrial_name_list[0].append(ind)
        elif name[:8] == "Flexray_": industrial_name_list[2].append(ind)
        elif name[:25] == "NXT Motion (specialized)_": industrial_name_list[1].append(ind)
        elif name[:28] == "Projection optics box (POB)_": industrial_name_list[3].append(ind)

    duedateList = [0]*4
    scheduleTimeList = [0]*4
    for i in range(4):
        counter = 0
        for ind in industrial_name_list[i]:
            if dfEDDF["schedulable"][ind]: 
                counter += 1
                duedateList[i] += float(dfEDDF["dueDatesCalculationTime"][ind])
                scheduleTimeList[i] += float(dfEDDF["schedulerTime"][ind])
        duedateList[i] /= counter
        scheduleTimeList[i] /= counter

    print("duedates: ", duedateList)
    print("scheduleTimes: ", scheduleTimeList)



    scedulability = [[0,0],[0,0]]
    makespanDifference = [0, 0, 0]
    makespan_EDDF = []
    makespan_ECF = []
    for ind in name_list:
        if dfEDDF["schedulable"][ind] and dfECF["schedulable"][ind]: 
            scedulability[0][0] += 1
            makespan_EDDF.append(dfEDDF["makespan"][ind])
            makespan_ECF.append(dfECF["makespan"][ind])
            if dfEDDF["makespan"][ind] < dfECF["makespan"][ind]: makespanDifference[0] += 1
            elif dfEDDF["makespan"][ind] > dfECF["makespan"][ind]: makespanDifference[1] += 1
            else: makespanDifference[2] += 1
                
        elif dfEDDF["schedulable"][ind] and not dfECF["schedulable"][ind]: scedulability[0][1] += 1
        elif not dfEDDF["schedulable"][ind] and dfECF["schedulable"][ind]: scedulability[1][0] += 1
        else: scedulability[1][1] += 1
        
    print(scedulability, makespanDifference)
    print(mcnemar(scedulability, exact=False, correction=False))
    print(stats.ttest_rel(makespan_EDDF, makespan_ECF))
main()