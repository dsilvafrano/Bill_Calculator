# Power balance of the selected system
# Packages required
import time
# starting time
start = time.time()
import pandas as pd
import numpy as np
import API
import SQL
import Inputs
import Monthly
import Monthwise

#Inputs required
solarp = pd.DataFrame()
solarp['AC(kW)'] = API.solarp['AC(kW)']
der_deg = Inputs.der_deg
load_input_type = Inputs.load_input_type
if load_input_type == "average_monthly":
    load = Monthly.user_load['Load']
else:
    load = Monthwise.user_load['Load']

n = len(load)
solar = Inputs.solar
battery = Inputs.battery
batstatus =Inputs.batstatus
socmax =Inputs.socmax
socin =Inputs.socin
socmin =SQL.socmin
metering_type =Inputs.metering_type

# power balance for the selected size
def power_balance(x1, g):
    # starting time
    start2 = time.time()
    # print(x1[0])
    # print(type(x1))
    # print(n)
    rem_load = np.zeros(n)
    exsolar = np.zeros(n)
    sol_cap = x1[0]
    # print(type(sol_cap))
    # print(sol_cap)
    # print(type(solarp))
    # print((solarp['load'][10]))


    # print('The solar capacity is:',sol_cap)
    solar_power = (solarp['AC(kW)'] * sol_cap) * (1 - (g * der_deg))
    # print((solar_power[10]))

    # print('The solar power generated:', sum(solar_power))
    # print(len(solar_power))
    bat_cap = x1[1]
    # print('The battery capacity is:',bat_cap)
    bat_inv = 0.835 * sol_cap
    ch_dis_available = np.zeros(n)
    soc = np.zeros(n)

    battery_power = np.zeros(n)
    gridp = np.zeros(n)
    gridpower = np.zeros(n)
    excessder = np.zeros(n)
    # load = annual_load_escalation(load_esc)[g]
    # print(len(user_load))
    # print('The load is :', load)

    #Power balance for Gross metering
    for i in range(0, 8760):
        # print('Load', user_load[i])
        # print('Solar', solar_power[i][0])
        # print(type(solar_power[i][0]))

    #Identifying the available remaining load & excess solar
        # if metering_type == "Gross Metering":
        #     rem_load[i] = load[i]
        #
        #     exsolar[i] = (solar_power[i])
        #     # print('Remaining load:', sum(rem_load))
        #     # print('Excess solar:', sum(exsolar))

        if (load[i] - (solar_power[i])) > 0:
            rem_load[i] = load[i] - solar_power[i]
        else:
            exsolar[i] = - load[i] + solar_power[i]

    # calculating charging/discharging power available
    if solar & battery:
        for i in range(n):
            if batstatus[0][i] == -1:
                if exsolar[i] < bat_inv:
                    ch_dis_available[i] = exsolar[i]
                else:
                    ch_dis_available[i] = bat_inv

            elif batstatus[0][i] == 1:
                if rem_load[i] < bat_inv:
                    ch_dis_available[i] = rem_load[i]
                else:
                    ch_dis_available[i] = bat_inv

        # calculating the state of charge based on min and max limit of soc
        socbatmax = socmax * bat_cap
        # print('SOC max', socbatmax)
        socbatmin = socmin * bat_cap
        # print('SOC min', socbatmin)
        soc[0] = socin * bat_cap
        # print('SOC initial', soc[0])

        for i in range(n - 1):
            k = i + 1
            if batstatus[0][k] == -1:
                if (ch_dis_available[k] + soc[k - 1]) < socbatmax:
                    soc[k] = ch_dis_available[k] + soc[k - 1]
                else:
                    soc[k] = socbatmax
            if batstatus[0][k] == 1:
                if (soc[k - 1] - ch_dis_available[k]) > socbatmin:
                    soc[k] = soc[k - 1] - ch_dis_available[k]
                else:
                    soc[k] = socbatmin
            elif batstatus[0][k] == 0:
                soc[k] = soc[k - 1]

            battery_power[k] = soc[k - 1] - soc[k]  # calculating actual battery discharging and charging power
            # print('Battery power:', (battery_power[0:48]))
        for i in range(0, 8760):
            if metering_type == "Gross Metering":
                gridp[i] = load[i]
                gridpower[i] = gridp[i]
                excessder[i] = (solar_power[i]) - battery_power[i]

            else :
                gridp[i] = load[i] - (solar_power[i]) - battery_power[i]  # allocating export and grid after battery
                if gridp[i] > 0:
                    gridpower[i] = gridp[i]
                    excessder[i] = 0
                elif gridp[i] < 0:
                    gridpower[i] = 0
                    excessder[i] = -gridp[i] # what happens if battery has remaining energy? Does it go to excess DER?
            # print(soc)
            # print(battery_power)
    else:
        if metering_type == "Gross Metering":
            gridpower = load
            excessder = solar_power
        else:
            gridpower = rem_load
            excessder = exsolar


    df1 = pd.DataFrame()
    df1['load'] = round(pd.DataFrame(load),3)
    df1['solar'] = round(solar_power,3)
    df1['grid'] = gridpower.round(3)
    df1['battery'] = battery_power.round(3)
    # print(df1['battery'][0:48])
    df1['excess'] = excessder.round(3)
    df1['rem load'] = rem_load.round(3)
    df1['exsolar'] = exsolar.round(3)
    df1['ch&dch'] = ch_dis_available.round(3)
    df1['SOC'] = soc.round(3)
    df1['batstatus'] = round(batstatus,3)

    sum_solar = sum(solar_power)
    sum_battery = sum(battery_power)
    sum_grid = sum(gridpower)
    sum_export = sum(excessder)
    if metering_type == "Gross Metering":
        sum_solar_load = 0
    else:
        sum_solar_load = sum_solar - sum_battery - sum_export

    # end time
    end2 = time.time()
    runtime2 = (end2 - start2)
    # print('The runtime for power balance is:',runtime2)
    # print('Total solar :', sum_solar)
    # print('Export:', sum(excessder))
    return df1, sum_battery, sum_grid, sum_export, sum_solar, sum_solar_load

# print('The power balance details:', sum(power_balance([20,10],1)[0]['battery'][0:48]))
# end time
end = time.time()

runtime = (end - start)
# print('The runtime power balance:', runtime)