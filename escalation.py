# Packages required
import time
# # starting time
# start1 = time.time()

import pandas as pd

from Inputs import load_input_type, sload, state_id, voltage_id, metering_id, tariff_id
from SQL import conn, load_esc, cost_esc
import Monthly
import Monthwise
from FC_EC_calc import slab_id_m

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

if load_input_type == "average_monthly":
    user_load = Monthly.user_load['Load']
    # print('Load', user_load)
else:
    user_load = Monthwise.user_load['Load']
    # print('Load', user_load)


# selection of appropriate slab with respect to the monthly avg consumption & escalating it accordingly
def slab_selection(list_s):
    avg_monthly = list_s[0]
    # print(avg_monthly)
    n = list_s[1]
    # print(n)
    # starting time
    start1 = time.time()
    # Selection of slab by taking a monthly average of 8760 points


    for s in range(1,slab_id_m+1 ):
        # print('Test')
        EC_t_q = pd.read_sql_query("select slab_id, period, tier, min, maximum, energy_charge,bill_amt from slabs_mapping where state_id =" + str(
                            state_id) + " and tarriff_type_id = " + str(
                            tariff_id) + " and voltage_type_id = " + str(
                            voltage_id) + " and metering_type_id = " + str(metering_id) + " and slab_id = " + str(
                            s), conn)
        EC_t = EC_t_q

        max_slab: float = EC_t['maximum'].max(0)
        # print('THe largest max is:', max_slab)
        min_slab: float = EC_t['min'].min(0)
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
    EC_matrix['energy_charge'] = temp_EC * (1 + (n * cost_esc))
    slab_id_a = EC_matrix['slab_id'].max()

    # Identify the TOU table
    # Peak TOU table
    TOU_p_q = pd.read_sql_query(
        "select period, tier, min, maximum, energy_charge,bill_amt from tou_period_energy_charge where tariff_type_id=" + str(
            tariff_id) + " and voltage_type_id=" + str(voltage_id) + " and state_id=" + str(
            state_id) + " and period=" + str(2), conn)
    TOU_p = TOU_p_q

    # Off peak TOU table
    TOU_op_q = pd.read_sql_query(
        "select period, tier, min, maximum, energy_charge,bill_amt from tou_period_energy_charge where tariff_type_id=" + str(
            tariff_id) + " and voltage_type_id=" + str(voltage_id) + " and state_id=" + str(
            state_id) + " and period=" + str(3), conn)
    TOU_op = TOU_op_q

    # Escalate the TOU peak charges
    EC_p_cost_esc = pd.DataFrame(TOU_p)
    # temp_EC_p = EC_p_cost_esc['energy_charge']
    # load_esc_years = [5, 10, 15, 20, 25]

    # for j in range(n, n + 1):
        # if j in load_esc_years:
        # print('The table is:', EC_cost_esc)
    temp_EC_p = EC_p_cost_esc['energy_charge']
    EC_p_cost_esc['energy_charge'] = temp_EC_p * (1 + (n * cost_esc))
    # slab_id_a = EC_p_cost_esc['slab_id'].max()
    # print('The applicable peak energy charge is:',(cost_escalation_p(1)))

    # Escalate the TOU off peak charges
    # def cost_escalation_op(n):
    EC_op_cost_esc = pd.DataFrame(TOU_op)
    # temp_EC_op = EC_op_cost_esc['energy_charge']
    # load_esc_years = [5, 10, 15, 20, 25]

    # for j in range(n, n + 1):
        # if j in load_esc_years:
        # print('The table is:', EC_cost_esc)
    temp_EC_op = EC_op_cost_esc['energy_charge']
    EC_op_cost_esc['energy_charge'] = temp_EC_op * (1 + (n * cost_esc))
    # slab_id_a = EC_p_cost_esc['slab_id'].max()

    # EC = pd.concat([EC_matrix,EC_p_cost_esc,EC_op_cost_esc], axis=0)
    # print(EC['period'][0][])
    # print('The applicable off peak energy charge is:',(cost_escalation_op(1)))
    # end time
    end1 = time.time()

    runtime1 = (end1 - start1)
    # print('The runtime slab selection inside:', runtime1)
    list_s_up = [EC_matrix, slab_id_a, EC_p_cost_esc, EC_op_cost_esc]
    return list_s_up

# print('The selected EC table is:', float(slab_selection(200, 0)[3]['energy_charge']))

# end time
# start = Monthly.start
# end = time.time()
# # #
# runtime = (end - start1)
#start time
# start = time.time()
# print('Result:', slab_selection([5000,0]))
# # end time
# end1 = time.time()
# runtime1 = (end1 - start)
# # print('The runtime Total:', runtime)
# print('The runtime Escalation:', runtime1)