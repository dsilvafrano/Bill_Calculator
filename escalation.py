# Packages required
import time
# # starting time
start1 = time.time()

import pandas as pd

import Inputs
import SQL
import Monthly
import Monthwise
import API
import FC_EC_calc

#SQL connection
conn = SQL.conn

# Inputs required
load_esc = SQL.load_esc
load_input_type = Inputs.load_input_type
cost_esc = SQL.cost_esc
# print(type(cost_esc))
fixed_charge_h = FC_EC_calc.fixed_charge_h
# print(type(fixed_charge_h))
slab_id_m = FC_EC_calc.slab_id_m
state_id = Inputs.state_id
voltage_id = Inputs.voltage_id
tariff_id = Inputs.tariff_id
metering_id = Inputs.metering_id
sload = Inputs.sload

if load_input_type == "average_monthly":
    user_load = Monthly.user_load['Load']
    # print('Load', user_load)
else:
    user_load = Monthwise.user_load['Load']
    # print('Load', user_load)


# # Apply escalation to annual load
# def annual_load_escalation(n):
#     annual_load = pd.DataFrame()
#     #Applying escalation for 25 years
#     # for n in range(0,26):
#     esc_load_n = user_load
#     esc_load_n = esc_load_n * (1 + (n * load_esc))
#     # annual_load.append(esc_load_n)
#     annual_load = esc_load_n
#     # print('Load',annual_load)
#     return annual_load

# print('The annual load for year:', sum(annual_load_escalation(0)))

# apply escalation to the fixed charge calculation
def fixed_charge_esc(n):
    FC = fixed_charge_h

    # for j in range(n, n+1):
    FC_esc = FC * (1 + (n * cost_esc))

    # print('The escalated fixed charge is:', FC_esc)

    return FC_esc
# print('The fixed charge is:', (fixed_charge_esc(0)))


# selection of appropriate slab with respect to the monthly avg consumption & escalating it accordingly
def slab_selection(avg_monthly, n):
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
            break
           # print('The EC slab is:', EC_matrix)

    # escalation of EC
    temp_EC = EC_matrix['energy_charge']
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
    temp_EC_p = EC_p_cost_esc['energy_charge']
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
    temp_EC_op = EC_op_cost_esc['energy_charge']
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

    return EC_matrix, slab_id_a, EC_p_cost_esc, EC_op_cost_esc

# print('The selected EC table is:', float(slab_selection(200, 0)[3]['energy_charge']))

# #build cost matrix for bill calculation
# def cost_matrix(n):
#     cost_matrix = []
#     cost_matrix_t = 0
#     EC_n =
#     if load_input_type == "average_monthly":
#         cons = Monthly.user_load['cumulative']
#         TOU = Monthly.user_load['TOU']
#         # print('Load', cons)
#     else:
#         cons = Monthwise.user_load['cumulative']
#         TOU = Monthwise.user_load['TOU']
#         # print('Load', cons)
#
#     for i in range (0,8760):
#         cost_matrix_t = float(slab_selection(cons[i], n)[0]['energy_charge']) if (TOU[i] == 1) \
#                             else float(slab_selection(cons[i], n)[2]['energy_charge']) if (TOU[i] == 2) \
#                             else float(slab_selection(cons[i], n)[3]['energy_charge'])
#         cost_matrix.append(cost_matrix_t)
#
#
#     return cost_matrix
#
# print('cost matrix:', cost_matrix(2))





# end time
# start = Monthly.start
end = time.time()
#
# runtime = (end - start)
runtime1 = (end - start1)
# print('The runtime Total:', runtime)
print('The runtime Escalation:', runtime1)