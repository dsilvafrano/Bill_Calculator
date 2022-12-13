#Calculate updated export units and billable units for Net Metering

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
def bill_unitsNM():
    bill_unit_25 = pd.DataFrame()

    ##Grid units : Has value for total, normal, peak & offpeak units
    g_units = (grid_w_sys25())
    g_units_t = g_units.loc[0]
    g_units_n = g_units.loc[1]
    g_units_p = g_units.loc[2]
    g_units_op = g_units.loc[3]
    print(g_units_t['year0'])
    print((g_units_n['year0']))
    print(g_units_p['year0'])
    print(g_units_op['year0'])
    # ##Solar, battery and export units
    a_units = (unit_w_sys25(esc25()[2], esc25()[3], esc25()[4]))
    e_units = a_units[2]
    units_25 = pd.DataFrame()
    print(e_units['year0'])
    n_units = []
    p_units = []
    op_units = []
    e_units_up = []
    for i in range(0,12):
        diff = (g_units_n['year0'][i] - e_units['year0'][i])
        if (diff > 0):
            n_units.append(diff)
            p_units[i] = g_units_p['year0'][i]
            op_units[i] = g_units_op['year0'][i]
            e_units_up[i] = 0
        else:
            diff1 = (g_units_p['year0'][i] - (-(diff)))
            if (diff1 > 0):
                n_units[i] = 0
                p_units[i] = diff1
                op_units[i] = g_units_op['year0'][i]
                e_units_up[i] = 0
            else:
                diff2 = (g_units_op['year0'][i] - (-(diff1)))
                if (diff2 > 0):
                    n_units[i] = 0
                    p_units[i] = 0
                    op_units[i] = diff2
                    e_units_up[i] = 0
                else:
                    e_units_up[i] = (-(diff2))

        units_25 = [n_units, p_units, op_units, e_units_up]
    print(units_25)
    return 'passed'

print(bill_unitsNM())

# end time
end = time.time()

runtime = (end - start)
print('The runtime Net Metering bill units:', runtime)