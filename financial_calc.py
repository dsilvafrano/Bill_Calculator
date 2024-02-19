# Financial calculation for the selected system

# Packages required
import time
# starting time

# from line_profiler import LineProfiler
import pandas as pd
import numpy as np
import numpy_financial as npf


from Inputs import metering_type, load_input_type, solarpv_subsidy, solar, battery, bat_type
import Monthly
import Monthwise

from Bill_w_o_sys25 import bill_w_o_sys25
from SQL import pysam_debt_fraction, cost_esc, loan_rate, loan_period,dis_factor, investmentcost_calculate,\
    replacement_cost, financial_fetch, tou_select, network_charge_fetch
from net_metering import NM
from net_feed_in import NF
from gross_metering import GM
from EC_select import EC_select


## Number of years for analysis
nyr = 26

def financial_calc(x1):
    start = time.time()
    if load_input_type == "average_monthly":
        Yr1_units_m = Monthly.monthly_data()
        Yr1_units = Yr1_units_m[0]
        # print('Avg_monthly', Yr1_units)
        Yr1_units_8760 = Yr1_units_m[4]
    else:
        Yr1_units_M = Monthwise.monthwise_data()
        Yr1_units = Yr1_units_M[0]
        Yr1_units_8760 = Yr1_units_M[4]
    #Converting in to 24 X 365 format
    Yr1_units_24x365_n = np.array(Yr1_units_8760)
    Yr1_units_24x365 = Yr1_units_24x365_n.reshape((365,24))
    # print('Montly load:',len(Yr1_units_24x365))
    # # amount invested calculation
    sol_cap = x1[0]
    bat_cap = x1[1]
    compensation_rate_t = network_charge_fetch(sol_cap)
    compensation_rate = compensation_rate_t[1]
    amount_invested = investmentcost_calculate(sol_cap, bat_cap)
    # print('The total installation cost is:', amount_invested)
    rep_batterycost, rep_invertercost = replacement_cost(sol_cap, bat_cap)
    loan_principal_amount = amount_invested * pysam_debt_fraction / 100
    eq_amount = amount_invested * (1 - (pysam_debt_fraction / 100))

    #Collecting Investment cost split up
    financial_costs = financial_fetch(sol_cap)
    solar_pv_cost = 0
    inverter_cost = 0
    battery_cost = 0
    subsidy_cost = 0
    if solar & battery:
        if bat_type == 1:
            solar_pv_cost = financial_costs[5]
            inverter_cost = financial_costs[4]
            battery_cost = financial_costs[6]
            subsidy_cost = solarpv_subsidy
        else:
            solar_pv_cost = financial_costs[5]
            inverter_cost = financial_costs[4]
            battery_cost = financial_costs[7]
            subsidy_cost = solarpv_subsidy
    else:
        solar_pv_cost = financial_costs[2]
        subsidy_cost = solarpv_subsidy

    # print('Solar cost:', (solar_pv_cost))
    # print('Inverter cost:', (inverter_cost))
    # print('Battery cost:', (battery_cost))
    # print('Subsidy cost:', (subsidy_cost))
    # average monthly/yearly cash flow
    # for base year
    cCF_t = np.zeros(nyr)
    CF = np.zeros(nyr)
    EC_avg_wo_DER = pd.DataFrame()
    Elec_bill_withoutDER_t = pd.DataFrame()
    Elec_bill_withDER_t = pd.DataFrame()
    Elec_bill_withoutDER = np.zeros(nyr)
    # fc_yearly_charge = np.zeros(nyr)
    Elec_bill_withDER = np.zeros(nyr)
    EC_avg_with_DER = pd.DataFrame()
    total_savings = np.zeros(nyr)
    total_op_cost = np.zeros(nyr)
    total_cost = np.zeros(nyr)
    total_debt_yearly = np.zeros(nyr)
    NPV_to_Savings: float = 0

    # starting time
    # start2 = time.time()
    Elec_bill_withoutDER_q = bill_w_o_sys25()
    Elec_bill_withoutDER_t = Elec_bill_withoutDER_q[0]
    # print('Bill without sys:',Elec_bill_withoutDER_t)
    Elec_bill_withoutDER[0] = sum(Elec_bill_withoutDER_t['year0'])
    EC_avg_wo_DER = sum(Elec_bill_withoutDER_q[1]['year0'])


    if metering_type == "Net Metering":
        EC = EC_select()
        EC_N = EC[0]
        EC_P = EC[1]
        EC_OP = EC[2]
        Elec_bill_withDER_T = NM(x1, EC_N, EC_P, EC_OP)
        Elec_bill_withDER_t = Elec_bill_withDER_T[0]
        g_unit_yr1 = sum(Elec_bill_withDER_T[5])
        s_unit_yr1 = Elec_bill_withDER_T[1]
        b_unit_yr1 = Elec_bill_withDER_T[4]
        e_unit_yr1 = Elec_bill_withDER_T[2]
        avg_annual_solar = (s_unit_yr1)/365
        # print('Solar:', s_unit_yr1)
        g_unit_yr1_8760 = (Elec_bill_withDER_T[5])
        # Converting in to 24 X 365 format
        Yr1_g_units_24x365_n = np.array(g_unit_yr1_8760)
        Yr1_g_units_24x365 = Yr1_g_units_24x365_n.reshape((365, 24))
        s_unit_yr1_8760 = (Elec_bill_withDER_T[6]['year0'])
        # Converting in to 24 X 365 format
        Yr1_s_units_24x365_n = np.array(s_unit_yr1_8760)
        Yr1_s_units_24x365 = Yr1_s_units_24x365_n.reshape((365, 24))
        b_unit_yr1_8760 = (Elec_bill_withDER_T[7]['year0'])
        # Converting in to 24 X 365 format
        Yr1_b_units_24x365_n = np.array(b_unit_yr1_8760)
        Yr1_b_units_24x365 = Yr1_b_units_24x365_n.reshape((365, 24))
        e_unit_yr1_8760 = (Elec_bill_withDER_T[8]['year0'])
        # Converting in to 24 X 365 format
        Yr1_e_units_24x365_n = np.array(e_unit_yr1_8760)
        Yr1_e_units_24x365 = Yr1_e_units_24x365_n.reshape((365, 24))
        EC_avg_with_DER = sum(Elec_bill_withDER_T[9]['year0'])
        # print('Grid:', sum(g_unit_yr1_8760))
        # print('Solar:', sum(s_unit_yr1_8760))
        # print('Battery:', sum(b_unit_yr1_8760))
        # print('export:', sum(e_unit_yr1_8760))
    elif metering_type == "Net Feed In":
        EC = EC_select()
        EC_N = EC[0]
        EC_P = EC[1]
        EC_OP = EC[2]
        Elec_bill_withDER_T = NF(x1, EC_N, EC_P, EC_OP)
        Elec_bill_withDER_t = Elec_bill_withDER_T[0]
        g_unit_yr1 = Elec_bill_withDER_T[3]
        s_unit_yr1 = Elec_bill_withDER_T[1]
        b_unit_yr1 = Elec_bill_withDER_T[4]
        e_unit_yr1 = Elec_bill_withDER_T[2]
        avg_annual_solar = (s_unit_yr1)/365
        g_unit_yr1_8760  = (Elec_bill_withDER_T[5])
        # Converting in to 24 X 365 format
        Yr1_g_units_24x365_n = np.array(g_unit_yr1_8760)
        Yr1_g_units_24x365 = Yr1_g_units_24x365_n.reshape((365, 24))
        s_unit_yr1_8760 = (Elec_bill_withDER_T[6][0]['year0'])
        # Converting in to 24 X 365 format
        Yr1_s_units_24x365_n = np.array(s_unit_yr1_8760)
        Yr1_s_units_24x365 = Yr1_s_units_24x365_n.reshape((365, 24))
        b_unit_yr1_8760 = (Elec_bill_withDER_T[6][1]['year0'])
        # Converting in to 24 X 365 format
        Yr1_b_units_24x365_n = np.array(b_unit_yr1_8760)
        Yr1_b_units_24x365 = Yr1_b_units_24x365_n.reshape((365, 24))
        e_unit_yr1_8760 = (Elec_bill_withDER_T[6][2]['year0'])
        # Converting in to 24 X 365 format
        Yr1_e_units_24x365_n = np.array(e_unit_yr1_8760)
        Yr1_e_units_24x365 = Yr1_e_units_24x365_n.reshape((365, 24))
        EC_avg_with_DER = sum(Elec_bill_withDER_T[7]['year0'])
        # print('Solar:', (g_unit_yr1))
        # print('Grid:', sum(g_unit_yr1_8760))
        # print('Solar:', sum(s_unit_yr1_8760))
        # print('Battery:', sum(b_unit_yr1_8760))
        # print('export:', sum(e_unit_yr1_8760))
    else:
        EC = EC_select()
        EC_N = EC[0]
        EC_P = EC[1]
        EC_OP = EC[2]
        Elec_bill_withDER_T = GM(x1, EC_N, EC_P, EC_OP)
        Elec_bill_withDER_t = Elec_bill_withDER_T[0]
        g_unit_yr1 = Elec_bill_withDER_T[3]
        s_unit_yr1 = Elec_bill_withDER_T[1]
        b_unit_yr1 = Elec_bill_withDER_T[4]
        e_unit_yr1 = Elec_bill_withDER_T[2]
        avg_annual_solar = (s_unit_yr1) / 365
        g_unit_yr1_8760 = (Elec_bill_withDER_T[5])
        # Converting in to 24 X 365 format
        Yr1_g_units_24x365_n = np.array(g_unit_yr1_8760)
        Yr1_g_units_24x365 = Yr1_g_units_24x365_n.reshape((365, 24))
        s_unit_yr1_8760 = (Elec_bill_withDER_T[6][0]['year0'])
        # Converting in to 24 X 365 format
        Yr1_s_units_24x365_n = np.array(s_unit_yr1_8760)
        Yr1_s_units_24x365 = Yr1_s_units_24x365_n.reshape((365, 24))
        b_unit_yr1_8760 = (Elec_bill_withDER_T[6][1]['year0'])
        # Converting in to 24 X 365 format
        Yr1_b_units_24x365_n = np.array(b_unit_yr1_8760)
        Yr1_b_units_24x365 = Yr1_b_units_24x365_n.reshape((365, 24))
        e_unit_yr1_8760 = (Elec_bill_withDER_T[6][2]['year0'])
        # Converting in to 24 X 365 format
        Yr1_e_units_24x365_n = np.array(e_unit_yr1_8760)
        Yr1_e_units_24x365 = Yr1_e_units_24x365_n.reshape((365, 24))
        EC_avg_with_DER = sum(Elec_bill_withDER_T[7]['year0'])
        # print('Solar:', (g_unit_yr1))
        # print('Grid:', sum(g_unit_yr1_8760))
        # print('Solar:', sum(s_unit_yr1_8760))
        # print('Battery:', sum(b_unit_yr1_8760))
        # print('export:', sum(e_unit_yr1_8760))


    # Year 0 is considered as BAU
    Elec_bill_withDER[0] = 0

    # end2 = time.time()
    # runtime2 = (end2 - start2)
    # print('The runtime for financial savings w sys is:', runtime2)
    total_op_cost[0] = 0# no escalation for O&M, must include
    total_cost[0] = 0
    total_savings[0] = 0
    CF[0] = (total_savings[0]) - total_cost[0]
    cCF = CF[0]
    cCF_t[0] = CF[0]

    # print('Elec_bill_withoutDER ', Elec_bill_withoutDER[0])
    # print('Elec_bill_withDER ', Elec_bill_withDER[0])

    emi = npf.pmt(loan_rate / 12, 12 * loan_period, -loan_principal_amount, 0)
    cum_cashflow: float = 0

    for i in range(1,26):# Building a 25 year analysis with first year as installation year
        # starting time
        # start3 = time.time()
        Elec_bill_withoutDER[i] = sum(Elec_bill_withoutDER_t['year' + str(i)])
        # starting time
        start1 = time.time()
        Elec_bill_withDER[i] = sum(Elec_bill_withDER_t['year' + str(i)])
        # print('THe bill with system year 1',Elec_bill_withDER[1] )
        # end time
        # end1 = time.time()
        # runtime1 = (end1 - start1)
        # print('The runtime for savings calculation is:',runtime1)
        if solar & battery:
            total_op_cost[i] = (500 * sol_cap + 500 * bat_cap) * (1 + (i * cost_esc))
        else:
            total_op_cost[i] = (500 * sol_cap ) * (1 + (i * cost_esc))
        # print('Total op cost year 2:', total_op_cost[2])
        # # # starting time
        # start1 = time.time()
        total_savings[i] = (Elec_bill_withoutDER[i] - Elec_bill_withDER[i])
        # # end time
        # end1 = time.time()
        # runtime1 = (end1 - start1)
        # print('The runtime for savings is:', runtime1)
        # print('Total saving:', total_savings)
        # print('inv:',rep_invertercost)
        # print('bat:',rep_batterycost)

        if i in range(2,12):
            total_debt_yearly[i] = 12 * emi

        if i == 1:
            total_cost[i] = eq_amount
        else:
            total_cost[i] = total_op_cost[i] + total_debt_yearly[i] + rep_invertercost[i] + rep_batterycost[i]

        CF[i] = total_savings[i] - total_cost[i]
        # print('Total saving:', total_savings[1])
        # print('Total cost:', total_cost[1])
        # print('The bill without sys:', Elec_bill_withoutDER)
        # print('The bill with sys:', Elec_bill_withDER)
        # print('The total savings is:', total_savings)
        # print('The total cost is:', total_cost)
        # print(CF)
        cCF = cCF + CF[i]
        cCF_t[i] = cCF

        cum_cashflow = cum_cashflow + CF[i]
    print('The cumulative CF is:', (cCF_t))
    # end3 = time.time()
    # runtime3 = (end3 - start3)
    # print('The runtime for financial bill w sys is:', runtime3)
    bau_npv: float = npf.npv(dis_factor, Elec_bill_withoutDER[1:nyr])
    bau_npv = (bau_npv + Elec_bill_withoutDER[0])

    dis_saving: float = npf.npv(dis_factor, total_savings[1:nyr])
    dis_saving = (dis_saving + total_savings[0])

    npv = npf.npv(dis_factor, CF[1:nyr])
    # print('NPV[1,24]:', npv)
    npv = npv + CF[0]
    # print('NPV:', npv)

    NPV_to_Savings = ((1 - (npv / bau_npv)) * 100)
    NPV_to_Savings = NPV_to_Savings

    # print(npv)
    cum_cashflow = cum_cashflow + CF[0]
    # print('cumcashflow:', cum_cashflow)

    average_annualcashflow = cum_cashflow / 25
    average_monthlycashflow = average_annualcashflow / 12
    # print('average_monthlycashflow:', average_monthlycashflow)

    # Shade free area 10m2 for 1kW panel
    shade_free_area = 10 * sol_cap

    # Contribution of solar, grid & battery

    sum_load = sum(Yr1_units)
    # print('sum of load', sum(Yr1_units))
    # sum_grid = sum(g_unit_yr1)
    # sum_solar = sum(s_unit_yr1)
    # sum_batt = sum(b_unit_yr1)
    # sum_export = sum(e_unit_yr1)
    # sum_load = sum_grid+sum_solar+sum_batt

    grid_contri = (g_unit_yr1/sum_load)*100
    # solar_contri = ((s_unit_yr1-b_unit_yr1) / sum_load) * 100
    # batt_contri = (b_unit_yr1 / sum_load) * 100
    if metering_type == "Gross Metering":
        solar_contri = 0
        batt_contri = 0
    else:
        solar_contri = ((s_unit_yr1 - b_unit_yr1 - e_unit_yr1) / sum_load) * 100
        batt_contri = (b_unit_yr1 / sum_load) * 100

    export_contri = (e_unit_yr1 / s_unit_yr1) * 100
    # grid_contri = g_unit_yr1
    # solar_contri = s_unit_yr1
    # batt_contri = b_unit_yr1
    # export_contri = e_unit_yr1
    print('Solar',(s_unit_yr1))
    print('Export',(e_unit_yr1))
    print('Battery', (b_unit_yr1))
    print('Grid',(g_unit_yr1))
    #Weighted average tariff BAU and DER
    # W_avg_EC_BAU = EC_avg_wo_DER
    W_avg_EC_BAU = EC_avg_wo_DER / sum_load
    # W_avg_EC_DER = EC_avg_with_DER
    W_avg_EC_DER = EC_avg_with_DER / g_unit_yr1
    # Emission factor CO2 yr 1
    Av_emission_CO2 = ((s_unit_yr1) * 0.793)/1000 # Emission factor for coal
    # Calculation of payback period
    payback_year = 0
    for i in range (0,26):
        if (cCF_t[i] < 0 and cCF_t[i+1]>0):
            payback_year = ((i) + (-cCF_t[i]/CF[i+1]))
            break
        elif cCF_t[i] > 0:
            payback_year = ((i) + (-cCF_t[i]/CF[i+1]))
            break

    total_savings_bill = sum(total_savings)
    roi = ((cum_cashflow) / sum(total_cost)) * 100 * (1 / 25)
    roi = roi
    # end time
    end = time.time()

    runtime = (end - start)
    print('The runtime Financial calculation:', runtime)

    return npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, \
           amount_invested, average_annualcashflow,avg_annual_solar,grid_contri,solar_contri,batt_contri,export_contri,\
           Av_emission_CO2, Yr1_units, Elec_bill_withoutDER,Elec_bill_withDER,shade_free_area, solar_pv_cost, \
           inverter_cost, battery_cost, subsidy_cost, tou_select, Yr1_units_24x365_n, Yr1_g_units_24x365, \
           Yr1_s_units_24x365, Yr1_b_units_24x365, Yr1_e_units_24x365, compensation_rate,W_avg_EC_BAU,W_avg_EC_DER

# print('The NPV is :',financial_calc([10,1]))
# profiler = LineProfiler()
# profiler.add_function(financial_calc)
#
# # Run the profiler
# profiler.runcall(financial_calc,[125,1])
#
# # print the results
# profiler.print_stats()
