#Calculate updated export units and billable units for Net Metering

# Packages required
import time
# starting time


import pandas as pd

from power_balance25 import esc25
from unit_w_sys25 import unit_w_sys25
from grid_w_sys25 import grid_w_sys25

# Function to do the bill calculation
def bill_unitsNM(x1):
    start = time.time()
    bill_unit_25 = pd.DataFrame()

    ##Grid units : Has value for total, normal, peak & offpeak units
    g_units_T = (grid_w_sys25(x1))
    g_units = (g_units_T[0])
    g_units_t = g_units.loc[0]
    g_units_n = g_units.loc[1]
    g_units_p = g_units.loc[2]
    g_units_op = g_units.loc[3]
    # print(g_units_t['year0'])
    # print((g_units_n['year0']))
    # print(g_units_p['year0'])
    # print(g_units_op['year0'])
    # ##Solar, battery and export units
    a_units_t = g_units_T[1]
    s_units_t = a_units_t[0]
    b_units_t = a_units_t[1]
    e_units_t = a_units_t[2]
    list = [a_units_t[0], a_units_t[1], a_units_t[2]]
    a_units = (unit_w_sys25(list))
    s_units = a_units[0]
    b_units = a_units[1]
    e_units = a_units[2]
    units_25 = pd.DataFrame()
    g_units_8760 = g_units_T[2]
    # print(e_units['year0'])
    for n in range(0,26):
        t_units = [0] * 12
        n_units = [0] * 12
        p_units = [0] * 12
        op_units = [0] * 12
        e_units_up = [0] * 12
        for i in range(0,12):
            diff = (g_units_n['year' + str(n)][i] - e_units['year' + str(n)][i])
            if (diff > 0):
                n_units[i] = diff
                p_units[i] = g_units_p['year' + str(n)][i]
                op_units[i] = g_units_op['year' + str(n)][i]
                e_units_up[i] = 0
            else:
                diff1 = (g_units_p['year' + str(n)][i] - (-(diff)))
                if (diff1 > 0):
                    n_units[i] = 0
                    p_units[i] = diff1
                    op_units[i] = g_units_op['year' + str(n)][i]
                    e_units_up[i] = 0
                else:
                    diff2 = (g_units_op['year' + str(n)][i] - (-(diff1)))
                    if (diff2 > 0):
                        n_units[i] = 0
                        p_units[i] = 0
                        op_units[i] = diff2
                        e_units_up[i] = 0
                    else:
                        e_units_up[i] = (-(diff2))
            t_units[i] = (n_units[i] + p_units[i] + op_units[i])
        units_25['year' + str(n)] = [t_units, n_units, p_units, op_units, e_units_up, s_units, b_units]
    # print(units_25)
    end = time.time()

    runtime = (end - start)
    print('The runtime Net Metering bill units:', runtime)
    return units_25, e_units, g_units_8760, s_units_t, b_units_t, e_units_t

# print(bill_unitsNM())

# end time
