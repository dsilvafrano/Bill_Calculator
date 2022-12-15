##Operation on df from power balance to find units in a month for 0 to 25 year
#Store it in dataframe for bill calculation
import time

# starting time
start = time.time()

# Packages required
import pandas as pd
import numpy as np
import Inputs
import API
import TOU
import calendar
from calendar import monthrange
from datetime import date as dt
from power_balance25 import esc25

# print('Entering grid units with system')

# TOU matrix
TOU = TOU.tou_matrix
# Retrieving dataframe with time stamp and days
# days = API.solarp['day']
TS = API.solarp['date&time']

def unit_w_sys25(list):
    units = pd.DataFrame()
    units = list[0]
    units_t = pd.DataFrame()
    units_t.insert(0, 'TS', TS)
    units_t.insert(1, 'TOU', TOU)
    units1 = list[1]
    units1_t = pd.DataFrame()
    units1_t.insert(0, 'TS', TS)
    units1_t.insert(1, 'TOU', TOU)
    units2 = list[2]
    # print(list[0:24])
    units2_t = pd.DataFrame()
    units2_t.insert(0, 'TS', TS)
    units2_t.insert(1, 'TOU', TOU)
    units_d = pd.DataFrame()
    temp = []
    temp1 = []
    temp2 = []
    for i in range(0, 26):
        units_m = pd.DataFrame()
        units1_m = pd.DataFrame()
        units2_m = pd.DataFrame()
        units_t['year'] = units['year' + str(i)]
        units1_t['year'] = units1['year' + str(i)]
        units2_t['year'] = units2['year' + str(i)]
        # units_t['cum_year'] = units_t.groupby((units_t['TS']).dt.month)['year'].cumsum()
        # data re-sampled based on each month(gives 12 values with sum for each month)
        sum_in_month = units_t.resample('MS', on='TS').year.sum()
        sum_in_month1 = units1_t.resample('MS', on='TS').year.sum()
        sum_in_month2 = units2_t.resample('MS', on='TS').year.sum()
        units_m['year' + str(i)] = sum_in_month
        units1_m['year' + str(i)] = sum_in_month1
        units2_m['year' + str(i)] = sum_in_month2
        # Appending the dataframes to a temporary list
        temp.append(units_m)
        temp1.append(units1_m)
        temp2.append(units2_m)
        # Joining the dataframes from the temporary list
    units_d = pd.concat(temp, axis=1)
    units1_d = pd.concat(temp1, axis=1)
    units2_d = pd.concat(temp2, axis=1)
    # print(units_d)
    return units_d, units1_d, units2_d

# print((unit_w_sys25(esc25()[2],esc25()[3],esc25()[4])))

# end time
end = time.time()

runtime = (end - start)
print('The runtime units with system 25 year:', runtime)


