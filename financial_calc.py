# Financial calculation for the selected system

# Packages required
import time
# starting time
start = time.time()

import pandas as pd
import numpy as np
import numpy_financial as npf


from Inputs import metering_type
from Bill_w_o_sys25 import bill_w_o_sys25
from SQL import pysam_debt_fraction, cost_esc, loan_rate, loan_period,dis_factor, investmentcost_calculate,\
    replacement_cost
from net_metering import NM
from net_feed_in import NF
from gross_metering import GM


## Number of years for analysis
nyr = 26

def financial_calc(x1):
    # # amount invested calculation
    sol_cap = x1[0]
    bat_cap = x1[1]
    amount_invested = investmentcost_calculate(sol_cap, bat_cap)
    print('The total installation cost is:', amount_invested)
    rep_batterycost, rep_invertercost = replacement_cost(sol_cap, bat_cap)
    loan_principal_amount = amount_invested * pysam_debt_fraction / 100
    eq_amount = amount_invested * (1 - (pysam_debt_fraction / 100))

    # average monthly/yearly cash flow
    # for base year
    cCF_t = np.zeros(nyr)
    CF = np.zeros(nyr)
    Elec_bill_withoutDER_t = pd.DataFrame()
    Elec_bill_withDER_t = pd.DataFrame()
    Elec_bill_withoutDER = np.zeros(nyr)
    # fc_yearly_charge = np.zeros(nyr)
    Elec_bill_withDER = np.zeros(nyr)
    total_savings = np.zeros(nyr)
    total_op_cost = np.zeros(nyr)
    total_cost = np.zeros(nyr)
    total_debt_yearly = np.zeros(nyr)
    NPV_to_Savings: float = 0

    # starting time
    start2 = time.time()

    Elec_bill_withoutDER_t = bill_w_o_sys25()
    Elec_bill_withoutDER[0] = sum(Elec_bill_withoutDER_t['year0'])

    if metering_type == "Net Metering":
        Elec_bill_withDER_t = NM(x1)
    elif metering_type == "Net Feed In":
        Elec_bill_withDER_t = NF(x1)
    else:
        Elec_bill_withDER_t = GM(x1)

    # Year 0 is considered as BAU
    Elec_bill_withDER[0] = 0

    end2 = time.time()
    runtime2 = (end2 - start2)
    print('The runtime for financial savings w sys is:', runtime2)
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
        start3 = time.time()
        Elec_bill_withoutDER[i] = sum(Elec_bill_withoutDER_t['year' + str(i)])
        # starting time
        start1 = time.time()
        Elec_bill_withDER[i] = sum(Elec_bill_withDER_t['year' + str(i)])
        # print('THe bill with system year 1',Elec_bill_withDER[1] )
        # end time
        end1 = time.time()
        runtime1 = (end1 - start1)
        # print('The runtime for savings calculation is:',runtime1)
        total_op_cost[i] = (500 * sol_cap + 500 * bat_cap) * (1 + (i * cost_esc))
        # print('Total op cost year 2:', total_op_cost[2])
        # # # starting time
        # start1 = time.time()
        total_savings[i] = (Elec_bill_withoutDER[i] - Elec_bill_withDER[i])
        # # end time
        # end1 = time.time()
        # runtime1 = (end1 - start1)
        # print('The runtime for savings is:', runtime1)
        # print('Total saving:', total_savings)

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
    # print('The cumulative CF is:', (cCF_t))
    end3 = time.time()
    runtime3 = (end3 - start3)
    print('The runtime for financial bill w sys is:', runtime3)
    bau_npv: float = npf.npv(dis_factor, Elec_bill_withoutDER[1:nyr])
    bau_npv = (bau_npv + Elec_bill_withoutDER[0])

    dis_saving: float = npf.npv(dis_factor, total_savings[1:nyr])
    dis_saving = (dis_saving + total_savings[0])

    npv = npf.npv(dis_factor, CF[1:nyr])
    # print('NPV[1,24]:', npv)
    npv = npv + CF[0]
    # print('NPV:', npv)

    NPV_to_Savings = ((npv / bau_npv) * 100)
    NPV_to_Savings = NPV_to_Savings

    # print(npv)
    cum_cashflow = cum_cashflow + CF[0]
    # print('cumcashflow:', cum_cashflow)

    average_annualcashflow = cum_cashflow / nyr
    average_monthlycashflow = average_annualcashflow / 12
    # print('average_monthlycashflow:', average_monthlycashflow)

    # Calculation of payback period
    payback_year = 0
    for i in range (0,26):
        if (cCF_t[i] < 0 and cCF_t[i+1]>0):
            payback_year = ((i) + (-cCF_t[i]/CF[i+1]))+1

    total_savings_bill = sum(total_savings)
    roi = ((cum_cashflow) / sum(total_cost)) * 100 * (1 / 25)
    roi = roi

    return npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, amount_invested

# print('The NPV is :',financial_calc(x1))

# end time
end = time.time()

runtime = (end - start)
print('The runtime Financial calculation:', runtime)