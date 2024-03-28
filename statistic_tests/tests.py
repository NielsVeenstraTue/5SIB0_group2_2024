from statsmodels.stats.contingency_tables import mcnemar
from scipy import stats

# McNemar test. Put in the table of feasible/infeasible. (Table III) in the paper
feasibility = [[254,336],[263,147]]
print(mcnemar(feasibility, exact=False, correction=False))


# paired sample t-test. Put in the makespans of the different schedulers
makespan_EDDF = [30, 31, 34, 40, 36, 35, 34, 30, 28, 29]
makespan_ECF = [30, 31, 32, 38, 32, 31, 32, 29, 28, 30]
print(stats.ttest_rel(makespan_EDDF, makespan_ECF))
