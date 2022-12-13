#Calculate the total bill when metering type is gross metering
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
def GM():
    # Units and Network charges information stored in variable
    g_units = grid_w_sys25()['year'+ str(0)]
    a_units = (unit_w_sys25(esc25()[2],esc25()[3],esc25()[4]))
    s_units = a_units[0]
    print(s_units['year1'])
    b_units = a_units[1]
    print(b_units['year1'])
    e_units = a_units[2]
    print(e_units['year1'])
    NC = network_charge_fetch(x1[0])[0]

    # # Fixed charge and Energy charge details
    # FC_m = FC_EC_calc.fixed_charge_m
    # EC = slab_selection(g_units[0], n)[0]
    # EC_p = slab_selection(g_units[0], n)[2]
    # EC_op = slab_selection(g_units[0], n)[3]
    # print(g_units[0])
    return 'passed'

print(GM())

# end time
end = time.time()

runtime = (end - start)
print('The runtime Gross metering:', runtime)