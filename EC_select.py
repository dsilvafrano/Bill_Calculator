# Packages required
import time
# # starting time
# start1 = time.time()

import pandas as pd
import Inputs
import SQL
from SQL import conn
from FC_EC_calc import slab_id_m

def EC_select():
    state_id = Inputs.state_id
    voltage_id = Inputs.voltage_id
    tariff_id = Inputs.tariff_id
    metering_id = Inputs.metering_id
    #EC selection
    EC_t_q = pd.read_sql_query(
        "select slab_id, period, tier, min, maximum, energy_charge,bill_amt from slabs_mapping where state_id =" + str(
            state_id) + " and tarriff_type_id = " + str(
            tariff_id) + " and voltage_type_id = " + str(
            voltage_id) + " and metering_type_id = " + str(metering_id), SQL.conn)
    #Whole EC slab for state,tariif, voltage and metering type
    EC_T = EC_t_q

    # if SQL.tou_select == 1 or SQL.tou_select == 2:
    # Peak TOU table
    TOU_p_q = pd.read_sql_query(
        "select period, tier, min, maximum, energy_charge,bill_amt from tou_period_energy_charge where tariff_type_id=" + str(
            tariff_id) + " and voltage_type_id=" + str(voltage_id) + " and state_id=" + str(
            state_id) + " and period=" + str(2), SQL.conn)
    TOU_p_T = TOU_p_q

    # Off peak TOU table
    TOU_op_q = pd.read_sql_query(
        "select period, tier, min, maximum, energy_charge,bill_amt from tou_period_energy_charge where tariff_type_id=" + str(
            tariff_id) + " and voltage_type_id=" + str(voltage_id) + " and state_id=" + str(
            state_id) + " and period=" + str(3), SQL.conn)
    TOU_op_T = TOU_op_q
    # else:
    #     TOU_p_T = 0
    #     TOU_op_T = 0
    # EC = pd.DataFrame()
    # EC = EC_T[EC_T['slab_id'] == 4]
    # EC = EC.reset_index(drop=True)
    return EC_T, TOU_p_T, TOU_op_T

# print('the EC table are',(EC_select()))