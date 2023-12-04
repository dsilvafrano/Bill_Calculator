## Retreive information from SQL Database

# Packages required
import pandas as pd
import numpy as np
import sqlite3
import logger
from Inputs import sload, state_id, voltage_id, metering_id, tariff_id, state, tariff, voltage, metering_type, solar, \
    battery, bat_type, residence_type, solarpv_subsidy, nyr
import time

# starting time
# start = time.time()

# create connection to DB
random_no = 0.3555
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("db23_updated.sqlite3")
    except ValueError as e:
        logger.debug(random_no + " " + e)
    return conn

conn = create_connection()


# fetch the dc ac ratio from database
dc_ac_ratio_q = pd.read_sql_query("select value from assumptions_pvwatts where parameter = 'dc_ac_ratio'", conn)
pysam_dc_ac_ratio = float(dc_ac_ratio_q.values[0])

# fetch the inverter replacement year from database
inv_replace_year_q = pd.read_sql_query("select value from assumptions_pvwatts where parameter = "
                                       "'inverter_replacement_year'", conn)
inv_replace_year = int(inv_replace_year_q.values[0])

# find the battery replacement year based on the lifecycle of batteries
if bat_type == 1:
    battery_cycle_q = pd.read_sql_query(
        "select value from assumptions_battwatts where parameter = 'battery_cyclelife_liion'", conn)

    battery_cycle_v = int(battery_cycle_q.values[0])
    battery_dod_q = pd.read_sql_query(
        "select value from assumptions_battwatts where parameter = 'battery_dod_liion'", conn)
    dod = int(battery_dod_q.values[0])/100
elif bat_type == 0:
    battery_cycle_q = pd.read_sql_query(
        "select value from assumptions_battwatts where parameter = 'battery_cyclelife_pbacid'", conn)
    battery_cycle_v = int(battery_cycle_q.values[0])
    battery_dod_q = pd.read_sql_query(
        "select value from assumptions_battwatts where parameter = 'battery_dod_pbacid'", conn)
    dod = int(battery_dod_q.values[0])/100
# print('DOD :', dod)

socmin = 1 - dod
# print('SOC min', socmin)
battery_replace_year = int(battery_cycle_v / 365)
numb_battery_replacement = int(nyr / (battery_replace_year + 1))
rep_yrs_battery = [i * (battery_replace_year + 1) for i in range(1, numb_battery_replacement + 1)]
rep_yrs_inverter = [inv_replace_year]

## loan related data
# debt fracton fetching from database
debt_fraction_q = pd.read_sql_query("select value from assumptions_cashloan where parameter = 'debt_fraction'", conn)
# logger.debug("pysam_debt_fraction ="+str((debt_fraction_q.values[0])))
pysam_debt_fraction = float(debt_fraction_q.values[0])

# Loan Rate from database
loan_rate_q = pd.read_sql_query("select value from assumptions_cashloan where parameter = 'loan_rate'", conn)
# logger.debug(random_no+" "+"loan_rate_q ="+str((loan_rate_q.values[0])))
loan_rate = float(loan_rate_q.values[0]) / 100

# loan period
loan_period_q = pd.read_sql_query("select value from assumptions_cashloan where parameter = 'loan_term'", conn)
# logger.debug(random_no+" "+"loan_rate_q ="+str((loan_rate_q.values[0])))
loan_period = float(loan_period_q.values[0])

# cost escalation/inflation rate
cost_esc_q = pd.read_sql_query("select value from assumptions_cashloan where parameter = 'inflation_rate'", conn)
# logger.debug(random_no+" "+"cost_esc_q ="+str((lcost_esc_q.values[0])))
cost_esc = cost_esc_q.values[0] / 100
# print('Cost escalation :', cost_esc)

# get discount rate for calculating npv
dis_factor_q = pd.read_sql_query("select value from assumptions_cashloan where parameter = 'real_discount_rate_show'",conn)
dis_factor = dis_factor_q.values[0] / 100
# print('Discount rate :', dis_factor)

# # cost escalation/inflation rate
# cost_esc_q = pd.read_sql_query("select value from assumptions_cashloan where parameter = 'inflation_rate'", conn)
# cost_esc = float(cost_esc_q.values[0] / 100)
# # print('Cost escalation :', cost_esc)

# load escalation
load_esc_q = pd.read_sql_query("select value from assumptions_grid where parameter = 'load_escalation'", conn)
load_esc = load_esc_q.values[0] / 100
# print('Load escalation:', load_esc)

#tou selection for case
tou_select_q = pd.read_sql_query("select applicability_periods from tou_applicability_periods where state_id=" + str(
                state_id) + " and tariff_type_id=" + str(tariff_id) + " and voltage_type_id=" + str(voltage_id), conn)
tou_select = int(tou_select_q.values[0])
# print(tou_select)

def tou_charge():
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
    return TOU_p, TOU_op
# Retrieve the Network charge and Compensation rate
def network_charge_fetch(user_pv_capacity):
    if state_id == 1 and voltage_id == 1:
        if float(user_pv_capacity) <= 10:
            network_charge_df = pd.read_sql_query("select network_charge from network_charge where state_id=" + str(
                state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
                tariff_id) + " and voltage_id=" + str(voltage_id) + " and max_pv=" + str(10), conn)
            comp_charge_df = pd.read_sql_query("select compensation_rate from network_charge where state_id=" + str(
                state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
                tariff_id) + " and voltage_id=" + str(voltage_id) + " and max_pv=" + str(10), conn)

        elif 10 < float(user_pv_capacity) <= 112:
            network_charge_df = pd.read_sql_query("select network_charge from network_charge where state_id=" + str(
                state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
                tariff_id) + " and voltage_id=" + str(voltage_id) + " and max_pv=" + str(112), conn)
            comp_charge_df = pd.read_sql_query("select compensation_rate from network_charge where state_id=" + str(
                state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
                tariff_id) + " and voltage_id=" + str(voltage_id) + " and max_pv=" + str(112), conn)

        else:
            network_charge_df = pd.read_sql_query("select network_charge from network_charge where state_id=" + str(
                state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
                tariff_id) + " and voltage_id=" + str(voltage_id) + " and max_pv=" + str(999), conn)

            comp_charge_df = pd.read_sql_query("select compensation_rate from network_charge where state_id=" + str(
                state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
                tariff_id) + " and voltage_id=" + str(voltage_id) + " and max_pv=" + str(999), conn)
    else:
        network_charge_df = pd.read_sql_query("select network_charge from network_charge where state_id=" + str(
            state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
            tariff_id) + " and voltage_id=" + str(voltage_id), conn)
        comp_charge_df = pd.read_sql_query("select compensation_rate from network_charge where state_id=" + str(
            state_id) + " and metering_type_id=" + str(metering_id) + " and tariff_id=" + str(
            tariff_id) + " and voltage_id=" + str(voltage_id), conn)

    network_charges = float(network_charge_df.values[0])
    compensation_rates = float(comp_charge_df.values[0])
    # print('compensation rate:', compensation_rates)
    # print('network_charges:', network_charges)

    return network_charges, compensation_rates
# print('The compensation rate & network charges are:', network_charge_fetch(10))

# Retrieve Financial suggestion
def financial_fetch(user_pv_capacity):
    df_for_state_id = pd.read_sql_query("select id from state WHERE name=" + f'"{state}"', conn)
    state_id = df_for_state_id['id'].values[0]

    df_for_consumer_id = pd.read_sql_query("select id from tariff_type WHERE name=" + f'"{tariff}"', conn)
    consumer_id = df_for_consumer_id['id'].values[0]

    df_for_voltage_id = pd.read_sql_query("select id from voltage_type WHERE name=" + f'"{voltage}"', conn)
    voltage_id = df_for_voltage_id['id'].values[0]

    df_for_metering_id = pd.read_sql_query(
        "select id from metering_type WHERE name=" + f'"{metering_type}"' + "and state_id = " + f'"{str(state_id)}"',
        conn);
    metering_id = df_for_metering_id['id'].values[0]

    # if df_for_max_pv.shape[0] == 0:
    df_max_pv = pd.read_sql_query(
        "select max_pv,min_pv,network_charge,compensation_rate from network_charge WHERE state_id=" + f'"{state_id}"' + " and tariff_id=" + f'"{consumer_id}"' + " and voltage_id=" + f'"{voltage_id}"' + " and metering_type_id=" + f'"{metering_id}"',
        conn)
    max_limit_pv = df_max_pv['max_pv'].max()
    min_limit_pv = df_max_pv['min_pv'].min()

    if max_limit_pv > float(sload):
        max_limit_pv = sload
    if str(metering_id) == "8":
        if min_limit_pv < float(sload):  # This is as SL for TN is 112kW and min capacity under Gross metering is 150kW
            min_limit_pv = 150

    df_for_cost_suggestion = pd.read_sql_query(
        "select capital_cost,inverter,pv_cost,hybrid_inverter,li_ion,lead_acid from cost_suggestion WHERE " + str(
            sload) + " between min_pv_cap and max_pv_cap",
        conn)

    max_limit_pv = str(max_limit_pv)
    min_limit_pv = str(min_limit_pv)
    capital_cost = str(df_for_cost_suggestion['capital_cost'].values[0])
    inverter_cost = str(df_for_cost_suggestion['inverter'].values[0])
    hybrid_inverter = str(df_for_cost_suggestion['hybrid_inverter'].values[0])
    pv_cost = str(df_for_cost_suggestion['pv_cost'].values[0])
    li_ion = str(df_for_cost_suggestion['li_ion'].values[0])
    lead_acid = str(df_for_cost_suggestion['lead_acid'].values[0])

    #     print('The capital cost is:', capital_cost)

    return max_limit_pv, min_limit_pv, capital_cost, inverter_cost, hybrid_inverter, pv_cost, li_ion, lead_acid
# print('The capital cost is:',financial_fetch(10)[2])

# Total investment cost
def investmentcost_calculate(system_capacity, bat_sim_kwh):
    # print('solar size:', system_capacity)
    if solar & battery:
        if bat_type == 1:
            if tariff == 'Domestic' and residence_type == 'Independent House' and system_capacity < 500:
                total_installation_cost = (float(system_capacity) * float(financial_fetch(sload)[5]) + float(bat_sim_kwh) * int(
                    financial_fetch(sload)[6]) + int(financial_fetch(sload)[4]) * float(system_capacity) / float(pysam_dc_ac_ratio)) - int(
                    solarpv_subsidy) * system_capacity
            else:
                total_installation_cost = (
                        (float(system_capacity) * float(financial_fetch(sload)[5])) + (float(bat_sim_kwh) * int(financial_fetch(sload)[6])) +
                        (int(financial_fetch(sload)[4]) * (float(system_capacity) / float(pysam_dc_ac_ratio))))
        else:
            if tariff == 'Domestic' and residence_type == 'Independent House' and system_capacity < 500:
                total_installation_cost = (float(system_capacity) * float(financial_fetch(sload)[5]) + float(bat_sim_kwh) * int(
                    financial_fetch(sload)[7]) + int(financial_fetch(sload)[4]) * float(system_capacity) / float(pysam_dc_ac_ratio)) - int(
                    solarpv_subsidy) * system_capacity
            else:
                total_installation_cost = (
                        (float(system_capacity) * float(financial_fetch(sload)[5])) + (float(bat_sim_kwh) * int(financial_fetch(sload)[7])) +
                        (int(financial_fetch(sload)[4]) * (float(system_capacity) / float(pysam_dc_ac_ratio))))
    else:
        if tariff == 'Domestic' and residence_type == 'Independent House' and system_capacity < 500:
            total_installation_cost = (float(system_capacity) * float(financial_fetch(sload)[2])) - int(
                solarpv_subsidy) * system_capacity
        else:
            total_installation_cost = (float(system_capacity) * float(financial_fetch(sload)[2]))

    return total_installation_cost
# print('The installation cost is:', investmentcost_calculate(10, 0))

# Replacement cost Calculation
# find the replacement cost of inverter and battery
def replacement_cost(system_capacity, bat_sim_kwh):
    rep_battery_cost = np.zeros(nyr)
    rep_inverter_cost = np.zeros(nyr)
    if bat_type == 1:
        battery_cost = float(financial_fetch(sload)[6])
    else:
        battery_cost = float(financial_fetch(sload)[7])

    if solar & battery:
        for k in range(0, nyr):
            i = k + 1
            if i in rep_yrs_battery:
                rep_battery_cost[k] = battery_cost * bat_sim_kwh
            if i in rep_yrs_inverter:
                rep_inverter_cost[k] = float(financial_fetch(sload)[3]) * system_capacity
    else:
        for k in range(0, nyr):
            i = k + 1
            if i in rep_yrs_inverter:
                rep_inverter_cost[k] = float(financial_fetch(sload)[3]) * system_capacity
    return rep_battery_cost, rep_inverter_cost
# print('The replacement costs are:',sum(replacement_cost(10, 0)[0]), sum(replacement_cost(10, 0)[1]) )

# # end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime SQL:', runtime)