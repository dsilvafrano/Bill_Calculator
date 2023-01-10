#Calculate the total bill when metering type is gross metering
# Packages required
import time
# starting time
start = time.time()

import pandas as pd
import numpy as np

import Inputs
from FC_EC_calc import fixed_charge_m
from power_balance25 import esc25
from unit_w_sys25 import unit_w_sys25
from grid_w_sys25 import grid_w_sys25
from SQL import network_charge_fetch, cost_esc
from EC_calc import EC

# Inputs required
x1 = np.zeros(2, dtype=float)
x1[0] = Inputs.x1[0] # user input solar capacity
x1[1] = Inputs.x1[1] # user input storage capacity

# Function to do the bill calculation
def GM():
    bill_amt_25 = pd.DataFrame()
    #Network charge and compensation rate
    NC = network_charge_fetch(x1[0])[0]
    CR = network_charge_fetch(x1[0])[1]

    # # Fixed charge and Energy charge details
    FC_m = fixed_charge_m
    ##Grid units : Has value for total, normal, peak & offpeak units
    g_units_t = (grid_w_sys25())
    # print((g_units[0][0]))
    ##Solar, battery and export units
    a_units_t = esc25()
    list = [a_units_t[2], a_units_t[3], a_units_t[4]]
    a_units = (unit_w_sys25(list))
    # print(a_units[0]['year25'])
    #Calculation of bill for 25 years
    for n in range(0,26):
        FC = FC_m * (1 + (n * cost_esc))
        # Units information stored in variable
        g_units = (g_units_t['year' + str(n)])
        s_units = a_units[0]['year' + str(n)]

        # print(s_units['year1'])
        # b_units = a_units[1]
        # print(b_units['year25'])
        # e_units = a_units[2]
        # print(e_units['year25'])
        bill_amt = 0
        temp = []
        bill_amt_m = []

    # #Calculation of bill for 12 months of a year
        for i in range(0,12):
            list_m = [g_units[0][i], g_units[1][i], g_units[2][i], g_units[3][i], n]
        #     # Variable for 25 year analysis
            EC_t = EC(list_m)
        # #Calculate the network charge applicable
            NC_t = NC * s_units[i]
            #Revenue from export to grid
            CR_t = CR * s_units[i]
            #Bill calculation for Gross metering
            bill_amt = FC + ((EC_t - CR_t) + NC_t)
            bill_amt_m.append(bill_amt)
        temp = bill_amt_m
        # print(bill_amt_m)
        bill_amt_25['year' + str(n)] = temp
    # print(bill_amt_25)
    return bill_amt_25

# print(GM())

# end time
end = time.time()

runtime = (end - start)
print('The runtime Gross metering:', runtime)