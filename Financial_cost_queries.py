## SQL queries to determine financial parameters

# Packages required
import pandas as pd
import numpy as np
from Inputs import sload, state_id, voltage_id, metering_id, tariff_id, state, tariff, voltage, metering_type, solar, \
    battery, bat_type, residence_type, solarpv_subsidy, nyr
import time
from SQL import pysam_dc_ac_ratio, rep_yrs_inverter, rep_yrs_battery, conn


# starting time
start = time.time()

# create connection with database

conn = conn

# Inputs required
state_id = state_id
voltage_id = voltage_id
tariff_id = tariff_id
metering_id = metering_id
state = state
tariff = tariff
voltage = voltage
metering_type = metering_type
sload = sload
solar = solar
battery = battery
bat_type = bat_type
residence_type = residence_type
pysam_dc_ac_ratio = pysam_dc_ac_ratio
solarpv_subsidy = solarpv_subsidy
nyr = nyr
rep_yrs_battery = rep_yrs_battery
rep_yrs_inverter = rep_yrs_inverter


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
print('The compensation rate & network charges are:', network_charge_fetch(10))

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
print('The capital cost is:',financial_fetch(10)[2])

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
print('The installation cost is:', investmentcost_calculate(10, 0))

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
print('The replacement costs are:',sum(replacement_cost(10, 0)[0]), sum(replacement_cost(10, 0)[1]) )

# end time
end = time.time()

runtime = (end - start)
print('The runtime is:', runtime)