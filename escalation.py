# Packages required
import time
# # starting time


import pandas as pd

from Inputs import load_input_type, sload, state_id, voltage_id, metering_id, tariff_id
from SQL import conn, load_esc, cost_esc, tou_charge
import Monthly
import Monthwise
from FC_EC_calc import slab_id_m
import numpy as np
#SQL connection
conn = conn

# Inputs required
load_esc = load_esc
load_input_type = load_input_type
cost_esc = cost_esc
slab_id_m = slab_id_m
state_id = state_id
voltage_id = voltage_id
tariff_id = tariff_id
metering_id = metering_id
sload = sload
#
# if load_input_type == "average_monthly":
#     user_load = Monthly.user_load['Load']
#     # print('Load', user_load)
# else:
#     user_load = Monthwise.user_load['Load']
#     # print('Load', user_load)


# selection of appropriate slab with respect to the monthly avg consumption & escalating it accordingly
def slab_selection(list_s):
    start = time.time()
    avg_monthly = list_s[0]
    # print(avg_monthly)
    n = list_s[1]
    # print(n)
    # starting time
    start1 = time.time()
    # Selection of slab by taking a monthly average of 8760 points
    EC_N = list_s[2]
    EC_P = list_s[3]
    EC_OP = list_s[4]

    for s in range(1,slab_id_m+1 ):
        # print('Test')
        EC_t = EC_N[EC_N['slab_id'] == s].reset_index(drop=True)
        # EC_t = EC_t.reset_index(drop=True)

        # max_slab: float = EC_t['maximum'].max(0)
        max_slab: float = np.max(EC_t['maximum'])
        # print('THe largest max is:', max_slab)
        # min_slab: float = EC_t['min'].min(0)
        min_slab: float = np.min(EC_t['min'])
        # print('The smallest min is:', min_slab)
        # print('The whole slab', EC_t)
        if float(max_slab) > float(avg_monthly) and float(avg_monthly) > float(min_slab):
            EC_matrix = EC_t
            # print(s)
            break
           # print('The EC slab is:', EC_matrix)
    # print(EC_matrix)
    # escalation of EC
    # temp_EC = EC_matrix['energy_charge']
    temp_EC = EC_matrix['energy_charge']
    # EC_matrix['energy_charge'] = temp_EC * (1 + (n * cost_esc))
    EC_matrix['energy_charge'] = temp_EC.apply(lambda x: x * (1 + n * cost_esc))

    slab_id_a = EC_matrix['slab_id'].max()

    # Identify the TOU table
    # Peak TOU table
    TOU_p = EC_P

    # Off peak TOU table
    TOU_op = EC_OP

    # Escalate the TOU peak charges
    EC_p_cost_esc = TOU_p
    temp_EC_p = EC_p_cost_esc['energy_charge']
    EC_p_cost_esc['energy_charge'] = temp_EC_p.apply(lambda x: x * (1 + n * cost_esc))


    # Escalate the TOU off peak charges
    EC_op_cost_esc = TOU_op

    temp_EC_op = EC_op_cost_esc['energy_charge']
    EC_op_cost_esc['energy_charge'] = temp_EC_op.apply(lambda x: x * (1 + n * cost_esc))

    list_s_up = [EC_matrix, slab_id_a, EC_p_cost_esc, EC_op_cost_esc]
    #end time
    end = time.time()
    runtime = (end - start)
    print('The runtime Escalation:', runtime)
    return list_s_up

# print('The selected EC table is:', float(slab_selection(200, 0)[3]['energy_charge']))

# end time
# start = Monthly.start

#start time
# start = time.time()
# print('Result:', slab_selection([5000,0]))
# # end time
# end1 = time.time()
# runtime1 = (end1 - start)
# # print('The runtime Total:', runtime)
