#Calculate the total bill when metering type is Net Metering
# Packages required
import time
# # starting time


import pandas as pd
import numpy as np

import Inputs
from FC_EC_calc import fixed_charge_m
from SQL import network_charge_fetch, cost_esc
from EC_calc import EC
from EC_select import EC_select
from bill_unitsNM import bill_unitsNM

# Inputs required
# x1 = np.zeros(2, dtype=float)
# x1[0] = Inputs.x1[0] # user input solar capacity
# x1[1] = Inputs.x1[1] # user input storage capacity

# Function to do the bill calculation
def NM(x1, EC_N, EC_P, EC_OP):
    start = time.time()
    # starting time
    # start1 = time.time()
    EC_avg25 = pd.DataFrame()
    bill_amt_25 = pd.DataFrame()
    bill_unit_25 = pd.DataFrame()
    # EC = EC_select()
    EC_N = EC_N
    EC_P = EC_P
    EC_OP = EC_OP
    #Network charge and compensation rate
    NC = network_charge_fetch(x1[0])[0]
    CR = network_charge_fetch(x1[0])[1]

    # # Fixed charge and Energy charge details
    FC_m = fixed_charge_m
    ##Bill units has value for Total, Normal, peak, offpeak, export and excess updated for each month
    bill_unit_25_T = bill_unitsNM(x1)
    bill_unit_25 = bill_unit_25_T[0]
    # print(sum(bill_unit_25['year0'][0]))
    e_unit_25 = bill_unit_25_T[1]
    g_units_8760 = bill_unit_25_T[2]
    s_units_8760 = bill_unit_25_T[3]
    b_units_8760 = bill_unit_25_T[4]
    e_units_8760 = bill_unit_25_T[5]
    e_unit_yr0 = e_unit_25
    # e_units = (e_unit_yr0['year0'])
    e_units_yr0 = sum(e_unit_yr0['year0'])
    g_units_yr0 = sum(bill_unit_25['year0'][0])




    s_units = bill_unit_25['year0'][5]
    s_units_yr0 = sum(s_units['year0'])
    b_units = bill_unit_25['year0'][6]
    b_units_yr0 = sum(b_units['year0'])
    # print(e_unit_yr0['year0'])
    # print(b_units['year25'])

    #Calculation of bill for 25 years
    for n in range(0,26):
        FC = FC_m * (1 + (n * cost_esc))
        # Units information stored in variable
        g_units = bill_unit_25['year' + str(n)]
        # print((g_units[0]))
        e_units = bill_unit_25['year' + str(n)][4]
        # print(e_units['year25'])
        bill_amt = 0
        temp = []
        bill_amt_m = []
        EC_avg =[]
    #
# #Calculation of bill for 12 months of a year
        for i in range(0,12):
            list_m = [g_units[0][i], g_units[1][i], g_units[2][i], g_units[3][i], n, EC_N, EC_P, EC_OP]
            # print(list_m)
        #     # Variable for 25 year analysis
        #     EC_t = EC(list_m)
            EC_T = EC(list_m)
            EC_t = EC_T[0]
            # ec_avg = EC_T[1]
            # #Calculate the network charge applicable
            NC_t = NC * s_units['year' + str(n)][i]
            #Revenue from export to grid
            # CR_t = CR * e_units[i]
            #Bill calculation for Gross metering
            bill_amt = FC + (EC_t + NC_t)
            bill_amt_m.append(bill_amt)
            EC_avg.append(EC_t)
        temp = bill_amt_m
        temp2 = EC_avg
        # print(temp)
        bill_amt_25['year' + str(n)] = temp
        EC_avg25['year' + str(n)] = temp2
    # print(s_units_yr0)
    # end time
    # end1 = time.time()
    #
    # runtime1 = (end1 - start1)
    # print('The runtime Net Metering inside:', i, runtime1)
    # end time
    end = time.time()

    runtime = (end - start)
    print('The runtime Net Metering:', runtime)
    return bill_amt_25, s_units_yr0, e_units_yr0, g_units_yr0,b_units_yr0, g_units_8760, s_units_8760, b_units_8760, \
           e_units_8760, EC_avg25

# print(NM([1,0]))

