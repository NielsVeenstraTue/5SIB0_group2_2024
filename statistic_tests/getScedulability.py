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
    for ind in dfECF.index:
        name = dfECF["name"][ind]
        if name[:11] == "NXT Motion_" and name[12] != "." : name_list.append(ind)
    
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