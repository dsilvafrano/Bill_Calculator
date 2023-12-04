# Power balance of the selected system
# Packages required
import time
# starting time
start = time.time()
import pandas as pd
import numpy as np
from SQL import socmin
from Inputs import solar,battery,socin,socmax,der_deg,batstatus,metering_type,load_input_type
import Monthly
import Monthwise
from API import api
from SOC import SOC

#Inputs required
der_deg = der_deg
load_input_type = load_input_type
if load_input_type == "average_monthly":
    load_m = Monthly.monthly_data()
    load = load_m[4]
else:
    load_M = Monthwise.monthwise_data()
    load = load_M[4]

n = len(load)
solar = solar
battery = battery
batstatus = batstatus[0]
socmax = socmax
socin = socin
socmin = socmin
metering_type = metering_type

# power balance for the selected size
def power_balance(x1,solarp, g):
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
    # for i in range(0, 8760):
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

        # if (load[i] - (solar_power[i])) > 0:
        #     rem_load[i] = load[i] - solar_power[i]
        # else:
        #     exsolar[i] = - load[i] + solar_power[i]

    # #Alternative method to determine remaining load and excess load
    rem_load = np.maximum(load - solar_power, 0)
    # # print('Remaining load:', len(rem_load))
    exsolar = np.maximum(solar_power - load, 0)
    # # print('Excess solar',len(exsolar))

    # calculating charging/discharging power available
    # if solar & battery:
    #     for i in range(n):
    #         if batstatus[0][i] == -1:
    #             if exsolar[i] < bat_inv:
    #                 ch_dis_available[i] = exsolar[i]
    #             else:
    #                 ch_dis_available[i] = bat_inv
    #
    #         elif batstatus[0][i] == 1:
    #             if rem_load[i] < bat_inv:
    #                 ch_dis_available[i] = rem_load[i]
    #             else:
    #                 ch_dis_available[i] = bat_inv
    ch_dis_available = np.where((solar & battery) & (batstatus == -1),np.minimum(exsolar, bat_inv),
        np.where((solar & battery) & (batstatus == 1),np.minimum(rem_load, bat_inv),0 ))
    # Default value if conditions are not met
    # print('Batstatus', batstatus[0][0:24])
    # print('Charge and discharge available:', (ch_dis_available[0:24]))
    # calculating the state of charge based on min and max limit of soc
    socbatmax = socmax * bat_cap
    # print('SOC max', socbatmax)
    socbatmin = socmin * bat_cap
    # print('SOC min', socbatmin)
    soc[0] = socin * bat_cap
    # print('SOC initial', soc[0])

    # for i in range(n - 1):
    #     k = i + 1
    #     if batstatus[0][k] == -1:
    #         if (ch_dis_available[k] + soc[k - 1]) < socbatmax:
    #             soc[k] = ch_dis_available[k] + soc[k - 1]
    #         else:
    #             soc[k] = socbatmax
    #     if batstatus[0][k] == 1:
    #         if (soc[k - 1] - ch_dis_available[k]) > socbatmin:
    #             soc[k] = soc[k - 1] - ch_dis_available[k]
    #         else:
    #             soc[k] = socbatmin
    #     elif batstatus[0][k] == 0:
    #         soc[k] = soc[k - 1]
    #
    #     battery_power[k] = soc[k - 1] - soc[k]  # calculating actual battery discharging and charging power

    # for k in range(1, n):
    #     if batstatus[k] == -1:
    #         soc[k] = min(ch_dis_available[k] + soc[k - 1], socbatmax)
    #     elif batstatus[k] == 1:
    #         soc[k] = max(soc[k - 1] - ch_dis_available[k], socbatmin)
    #     else:
    #         soc[k] = soc[k - 1]
    #
    #     battery_power[k] = soc[k - 1] - soc[k]
    # battery_power = np.where(battery_power<0, 0, battery_power)
    battery_power = SOC(ch_dis_available,x1)
    # print('SOC', soc[0:24])
    # print('Battery power:', (battery_power[0:72]).round(3))
    # for i in range(0, 8760):
    if metering_type == "Gross Metering":
        # print('enter GM')
        # gridp[i] = load[i]
        gridpower = load
        excessder = (solar_power) - battery_power

    else :
        # print('enter Not GM')
        gridp = load - (solar_power) - battery_power  # allocating export and grid after battery
        gridpower = np.where(gridp > 0, gridp,0)
        excessder = np.where(gridp < 0,-gridp,0)
        # if gridp[i] > 0:
        #     gridpower[i] = gridp[i]
        #     excessder[i] = 0
        # elif gridp[i] < 0:
        #     gridpower[i] = 0
        #     excessder[i] = -gridp[i] # what happens if battery has remaining energy? Does it go to excess DER?
        # print(gridpower[0:24])
        # print(excessder[0:24])
    # else:
    #     # print('Alt else')
    #     if metering_type == "Gross Metering":
    #         # print('Enter gm')
    #         gridpower = load
    #         excessder = solar_power
    #     else:
    #         # print('Enter not gm')
    #         gridpower = rem_load
    #         excessder = exsolar

    # print('Load', load[0:24])
    # print('grid', gridpower[0:24])
    # print('solar',solar_power[0:24])
    # print('battery',battery_power[0:24].round(3))
    # print('export',excessder[0:24])
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
        sum_solar_load = sum_solar - sum_export

    # end time
    end2 = time.time()
    runtime2 = (end2 - start2)
    # print('The runtime for power balance is:',runtime2)
    # print('Total solar :', sum_solar)
    # print('Export:', sum(excessder))
    return df1, sum_battery, sum_grid, sum_export, sum_solar, sum_solar_load

# solarp = api()
# # Converting (Wac) to (kWac)
# solarp['AC(kW)'] = solarp['AC(kW)']/1000
# #
# print('The power balance details:', power_balance([1,1],solarp,0))
# end time
end = time.time()

runtime = (end - start)
# print('The runtime power balance:', runtime)