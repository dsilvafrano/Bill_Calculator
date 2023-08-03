#Packages required
import time
# starting time
start = time.time()
import numpy as np
import pandas as pd
from financial_calc import financial_calc
from Inputs import solar, battery, sload

# Customise run inputs and results display
a =np.zeros(2, dtype=float).round(3)
a[0] = 1  # user input solar capacity
# # a[0]= 26.126338006179388 # user input solar capacity
if solar & battery:
    a[1]= 1 # user input storage capacity
else:
    a[1] = 2  # user input storage capacity
npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, amount_invested\
    ,  average_annualcashflow,s_unit_yr1,grid_contri,solar_contri,batt_contri,export_contri, Av_emission_CO2, \
    Yr1_units, Elec_bill_withoutDER,Elec_bill_withDER,shade_free_area, solar_pv_cost, inverter_cost, battery_cost, \
    subsidy_cost,tou_select, Yr1_units_24x365, Yr1_g_units_24x365, Yr1_s_units_24x365, Yr1_b_units_24x365, \
    Yr1_e_units_24x365 =financial_calc(a)

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
print('TOU Applicability:', str(tou_select))
print('24x365 matrix: Load', Yr1_units_24x365)
print('24x365 matrix: To load from Grid', Yr1_g_units_24x365)
print('24x365 matrix: To load from Solar', Yr1_s_units_24x365)
print('24x365 matrix: To load from Battery', Yr1_b_units_24x365)
print('24x365 matrix: To grid from System ', Yr1_e_units_24x365)
a1 = [a[0], a[1], npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings,
      amount_invested,average_annualcashflow,s_unit_yr1, Av_emission_CO2, sum(Yr1_units), (Elec_bill_withoutDER),(Elec_bill_withDER)]
# print(a1)


# end time
end = time.time()

runtime = (end - start)
print('The runtime for Optimiser is:', runtime)