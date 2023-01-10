#Operation on df_g from power balance to find normal, peak & off peak units in a month for 0 to 25 year
#Store it in dataframe for bill calculation
import time

# starting time
start = time.time()

# Packages required
import pandas as pd
import numpy as np
from Inputs import wk,ts
from TOU import tou_matrix
from power_balance25 import esc25

# print('Entering grid units with system')

# TOU matrix
TOU = tou_matrix
# Retrieving dataframe with time stamp and days
days = wk
TS = ts

def grid_w_sys25():
    g_units = pd.DataFrame()
    g_units = esc25()[1]
    g_units_t = pd.DataFrame()
    g_units_t.insert(0, 'TS', TS)
    g_units_t.insert(1, 'TOU', TOU)
    g_units_d = pd.DataFrame()
    temp = []
    for i in range(0, 26):
        g_units_m = pd.DataFrame()
        g_units_t['year'] = g_units[['year' + str(i)]]
        #cumulating the load for each month
        # g_units_t['cum_Load_year'] = g_units_t.groupby((g_units_t['TS']).dt.month)['year'].cumsum()
        #filter for normal period and cumulating for each month
        g_units_t['normal_year'] = np.where(g_units_t['TOU'] == 1, g_units_t['year'], 0)
        # print(g_units_t[0:24])
        # g_units_t['cum_N_year'] = g_units_t.groupby((g_units_t['TS']).dt.month)['normal_year'].cumsum()
        # filter for peak period and cumulating for each month
        g_units_t['peak_year'] = np.where(g_units_t['TOU'] == 2, g_units_t['year'], 0)
        # g_units_t['cum_P_year'] = g_units_t.groupby((g_units_t['TS']).dt.month)['peak_year'].cumsum()
        # filter for offpeak period and cumulating for each month
        g_units_t['offpeak_year'] = np.where(g_units_t['TOU'] == 3, g_units_t['year'], 0)
        # g_units_t['cum_OP_year'] = g_units_t.groupby((g_units_t['TS']).dt.month)['offpeak_year'].cumsum()

        # data re-sampled based on each month(gives 12 values with sum for each month)
        sum_in_month = g_units_t.resample('MS', on='TS').year.sum()
        sum_in_month_n = g_units_t.resample('MS', on='TS').normal_year.sum()
        sum_in_month_p = g_units_t.resample('MS', on='TS').peak_year.sum()
        sum_in_month_op = g_units_t.resample('MS', on='TS').offpeak_year.sum()


        g_units_m['year'+ str(i)] = [sum_in_month, sum_in_month_n, sum_in_month_p, sum_in_month_op]
        #Appending the dataframes to a temporary list
        temp.append(g_units_m)
    #Joining the dataframes from the temporary list
    g_units_d = pd.concat(temp, axis=1)

    # print(g_units_d['year25'][3])

    return g_units_d

# print((grid_w_sys25()))


# end time
end = time.time()

runtime = (end - start)
print('The runtime grid with system 25 year:', runtime)