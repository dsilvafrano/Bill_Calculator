#Calculate the total bill when metering type is Net Metering
# Packages required
import time
# starting time
start = time.time()

import pandas as pd
import numpy as np

import Inputs
import SQL
import Monthly
import Monthwise
import API
import TOU
import FC_EC_calc
from escalation import slab_selection
from power_balance25 import esc25
from unit_w_sys25 import unit_w_sys25
from grid_w_sys25 import grid_w_sys25
from SQL import network_charge_fetch
from EC_calc import EC
#SQL connection
conn = SQL.conn

# Inputs required
x1 = np.zeros(2, dtype=float)
x1[0] = Inputs.x1[0] # user input solar capacity
x1[1] = Inputs.x1[1] # user input storage capacity
load_esc = SQL.load_esc
cost_esc = SQL.cost_esc
tou_select = SQL.tou_select
# print(tou_select)
# TOU matrix
TOU = TOU.tou_matrix
# Function to do the bill calculation
def NM():
    bill_amt_25 = pd.DataFrame()
    #Network charge and compensation rate
    NC = network_charge_fetch(x1[0])[0]
    CR = network_charge_fetch(x1[0])[1]

    # # Fixed charge and Energy charge details
    FC_m = FC_EC_calc.fixed_charge_m
    ##Grid units : Has value for total, normal, peak & offpeak units
    g_units_t = (grid_w_sys25())
    # print((g_units[0][0]))
    ##Solar, battery and export units
    a_units = (unit_w_sys25(esc25()[2], esc25()[3], esc25()[4]))
    print(g_units_t)
    # print(a_units[0]['year' + str(0)])
    # print(a_units[1]['year' + str(0)])
    # print(a_units[2]['year' + str(0)])
    ##Difference of grid units and export units
    d_units = g_units_t['year0'][0] - a_units[2]['year0']
    # print(d_units)
    # print(a_units[0]['year25'])
    #Calculation of bill for 25 years
    # for n in range(0,26):
    #     # Units information stored in variable
    #     g_units = (g_units_t['year' + str(n)])
    #     s_units = a_units[0]['year' + str(n)]
    #     # print(s_units['year1'])
    #     b_units = a_units[1]['year' + str(n)]
    #     # print(b_units['year25'])
    #     e_units = a_units[2]['year' + str(n)]
    #     # print(e_units['year25'])
    #     bill_amt = 0
    #     temp = []
    #     bill_amt_m = []
    #
    # # #Calculation of bill for 12 months of a year
    #     for i in range(0,12):
    #     #     # Variable for 25 year analysis
    #         EC_t = EC(g_units[0][i], g_units[1][i], g_units[2][i], g_units[3][i], n)
    #     # #Calculate the network charge applicable
    #         NC_t = NC * s_units[i]
    #         #Revenue from export to grid
    #         CR_t = CR * e_units[i]
    #         #Bill calculation for Gross metering
    #         bill_amt = FC_m + ((EC_t - CR_t) + NC_t)
    #         bill_amt_m.append(bill_amt)
    #     temp = bill_amt_m
    #     # print(bill_amt_m)
    #     bill_amt_25['year' + str(n)] = temp
    # print(bill_amt_25)
    return 'passed'

print(NM())

# end time
end = time.time()

runtime = (end - start)
print('The runtime Net Metering:', runtime)