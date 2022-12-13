# Packages required
import numpy as np
import pandas as pd
import Inputs
import SQL
import time

# starting time
# start = time.time()

#SQL connection
conn = SQL.conn

# Inputs required
state_id = Inputs.state_id
voltage_id = Inputs.voltage_id
tariff_id = Inputs.tariff_id
metering_id = Inputs.metering_id
sload = Inputs.sload

# Retrieve the applicable Energy charge; max slab & max tier
slab_id_q = pd.read_sql_query("select slab_id, period, tier, min, maximum, energy_charge from slabs_mapping where state_id =" 
                              + str(state_id) + " and tarriff_type_id = " + str(tariff_id) + " and voltage_type_id = " 
                              + str(voltage_id) + " and metering_type_id = " + str(metering_id),conn)
slab_id_t = slab_id_q
# print('The EC table is:', slab_id_t)
slab_id_m = slab_id_t['slab_id'].max()
# print('The max slab is', slab_id_m)
tier_m = slab_id_t['tier'].max()
# print('The tier slab is', tier_m)


# Retrieving fixed charge and calculate hourly fixed charge & monthly fixed charge
charge_calculation_q = pd.read_sql_query("select charge_calculation from fixedcharge where tariff_id=" + str(tariff_id)
                                         + " and voltage_id=" + str(voltage_id) + " and state_id=" + str(state_id),
                                         conn)
charge_calculation = int(charge_calculation_q.values[0])
if int(charge_calculation) == 0:
    fixed_charge = 0
elif charge_calculation == 1:
    fixed_charges_q = pd.read_sql_query("select fixed_charge from fixedcharge where state_id =" + str(state_id)
                                        + " and voltage_id = " + str(voltage_id), conn)
    fixed_charge = float(fixed_charges_q.values[0])
elif charge_calculation == 2:

    # Check if the fixed charge table has tiers
    tier_check_q = pd.read_sql_query(
        "select tier from fixedcharge where tariff_id=" + str(tariff_id) + " and voltage_id="
        + str(voltage_id) + " and state_id=" + str(state_id), conn)
    tier_check = tier_check_q
    # print('Tier check:', tier_check)
    max_tier_check = tier_check['tier'].max()
    # print('Max tier check:', max_tier_check)
    min_tier_check = tier_check['tier'].min()
    # print('Min tier check:', min_tier_check)

    # Retrieve fixed charge from DB and calculation
    if max_tier_check == 1:
        fixed_charges_q = pd.read_sql_query(
            "select fixed_charge from fixedcharge where tariff_id=" + str(tariff_id) + " and voltage_id=" + str(
                voltage_id) + " and state_id=" + str(state_id), conn)
        fixed_charge = float(fixed_charges_q.values[0])
        # print('FC:', fixed_charge)
        fixed_charge = fixed_charge * sload
    else:
        sl_check_q = pd.read_sql_query("select fixed_charge, sanctioned_load from fixedcharge where tariff_id=" + str(
            tariff_id) + " and voltage_id=" + str(voltage_id) + " and state_id=" + str(state_id), conn)
        sl_fc_check = sl_check_q
        # print('SL:', sl_fc_check)
        # print('FC:', sl_fc_check['fixed_charge'])
        # print('SL:', sl_fc_check['sanctioned_load'][1])

        fixed_charge = 0
        fc_sl = sload
        fc_temp = 0
        for i in range(0, len(sl_fc_check)):
            # print('new sl value:', fc_sl)
            if fc_sl >= float(sl_fc_check['sanctioned_load'][i]):
                fc_temp = fc_temp + (sl_fc_check['fixed_charge'][i] * sl_fc_check['sanctioned_load'][i])
                fc_sl = fc_sl - float(sl_fc_check['sanctioned_load'][i])
                fc_sl = fc_sl
                # print('FC temp:', fc_sl)
            else:
                fc_temp = fc_temp + (sl_fc_check['fixed_charge'][i] * fc_sl)
                fc_sl = fc_sl - fc_sl
            # print('FC value:', fc_temp)
        fixed_charge = fc_temp
        fixed_charge = fixed_charge

fixed_charge_a = fixed_charge * 12
fixed_charge_m = fixed_charge
fixed_charge_h = fixed_charge_a / 8760

# print("fixed charge =", str(fixed_charge))
# print("fixed charge annual =", str(fixed_charge_a))
# print("fixed charge per hour =", str(fixed_charge_h))

# end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime FC & EC:', runtime)