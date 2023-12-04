#Packages required
import time
# starting time
start = time.time()
import numpy as np
import pandas as pd
from financial_calc import financial_calc
from Inputs import solar, battery, sload, x1
import matplotlib
from matplotlib import pyplot as plt
# from pyplot import plot
from mpl_toolkits.mplot3d import Axes3D

# Customise run inputs and results display
a =np.zeros(2, dtype=float).round(3)
a[0] = x1[0] #15 # user input solar capacity
# # a[0]= 26.126338006179388 # user input solar capacity
if solar & battery:
    a[1]= x1[1]#1 # user input storage capacity
else:
    a[1] = 0  # user input storage capacity
npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, amount_invested\
    ,  average_annualcashflow,s_unit_yr1,grid_contri,solar_contri,batt_contri,export_contri, Av_emission_CO2, \
    Yr1_units, Elec_bill_withoutDER,Elec_bill_withDER,shade_free_area, solar_pv_cost, inverter_cost, battery_cost, \
    subsidy_cost,tou_select, Yr1_units_24x365_n, Yr1_g_units_24x365, Yr1_s_units_24x365, Yr1_b_units_24x365, \
    Yr1_e_units_24x365,compensation_rate,W_avg_EC_BAU,W_avg_EC_DER =financial_calc(a)

# end = time.time()
# # total time taken
# print(f"Runtime of the program is {end - start}")
# runtime = (end - start)

print('Solar PV capacity(kW):', a[0])
print('Battery energy capacity(kWh):', a[1])
print('NPV = ' + str(npv))
print('payback year = ' + str(payback_year))
print('25 yr savings = ' + str(cum_cashflow))
print('return on investment = ' + str(roi))
print('% of savings in 25 yrs = ' + str((cum_cashflow/sum(Elec_bill_withoutDER))*100))
print('Grid contribution = ' + str(grid_contri))
print('Solar contribution = ' + str(solar_contri))
print('Batt contribution = ' + str(batt_contri))
print('Export contribution = ' + str(export_contri))
print('NPV(BAU) to dis.Savings = ' + str(100-NPV_to_Savings))
print('Shade free area(m2) = ' + str(shade_free_area))
print('Avg. annual Savings = ' + str(average_annualcashflow))
print('Avg. solar gen for yr 1 = ' + str(s_unit_yr1))
print('Av_emission_CO2 for yr 1 = ' + str(Av_emission_CO2))
print('Load for yr 1 = ' + str(sum(Yr1_units)))
print('Electric bill w/o sys =' + str((Elec_bill_withoutDER)))
print('Electric bill w sys =' + str((Elec_bill_withDER)))
print('Solar cost:', str(solar_pv_cost))
print('Inverter cost:', str(inverter_cost))
print('Battery cost:', str(battery_cost))
print('Subsidy cost:', str(subsidy_cost))
print('Amount invested:', str(amount_invested))
print('TOU Applicability:', str(tou_select))
print('Compensation rate (INR/kWh):',compensation_rate)
print('Average tariff - BAU case (INR/kWh):',W_avg_EC_BAU)
print('Average tariff - DER case (INR/kWh):', W_avg_EC_DER)
print('24x365 matrix: Load', sum(Yr1_units_24x365_n))
print('24x365 matrix: To load from Grid', Yr1_g_units_24x365[0])
print('24x365 matrix: To load from Solar', Yr1_s_units_24x365[0])
print('24x365 matrix: To load from Battery', Yr1_b_units_24x365[0])
print('24x365 matrix: To grid from System ', Yr1_e_units_24x365[0])
a1 = [a[0], a[1], npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings,
      amount_invested,average_annualcashflow,s_unit_yr1, Av_emission_CO2, sum(Yr1_units), (Elec_bill_withoutDER),(Elec_bill_withDER)]
# print(a1)

#Creating graph for load
#
# fig = plt.figure(figsize=(10,5))
#
#
# x = Yr1_units_24x365_n
# print('L', x)
# xpoints = np.array(x)
# print('x',xpoints[0:24])
# # ypoints = np.array([1,8760])
# # print('y',ypoints)
# plt.plot(xpoints[48:72])
# # Set intervals and show values on the x-axis
# plt.xticks(np.arange(0, 24, step=1))  # Set x-axis tick positions at intervals of 2
# plt.xlabel('Time(hrs)')
#
# # Set intervals and show values on the y-axis
# plt.yticks(np.arange(0, 0.7, step=0.1))  # Set y-axis tick positions at intervals of 0.5
# plt.ylabel('Load(kWh)')
# # plt.fill_between(xpoints)
# plt.show()
# end time
end = time.time()

runtime = (end - start)
print('The runtime for Optimiser is:', runtime)