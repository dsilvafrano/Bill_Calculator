# Calculate the monthly bill without system

# Packages required
import time
# starting time


import pandas as pd

from Inputs import load_input_type
from SQL import conn, load_esc, cost_esc, tou_select
# from Monthly import avg_in_month_m, avg_in_month_m_n, avg_in_month_m_p, avg_in_month_m_op
import Monthly
# using 'from monthwise' results in same variable, giving incorrect results, hence retained the below call method
import Monthwise
from FC_EC_calc import fixed_charge_m
from EC_calc import EC

# Function to do the bill calculation
def bill_w_o_sys(n,EC_N,EC_P,EC_OP):
    start = time.time()
    if load_input_type == "average_monthly":
        monthly_units = Monthly.monthly_data()
        month_units = monthly_units[0]
        month_units_n = monthly_units[1]
        month_units_p = monthly_units[2]
        month_units_op = monthly_units[3]
        # print('Units', month_units)
    else:
        Monthly_units = Monthwise.monthwise_data()
        month_units = Monthly_units[0]
        month_units_n = Monthly_units[1]
        month_units_p = Monthly_units[2]
        month_units_op = Monthly_units[3]
        # print('Units', month_units)


    # m_units = 1000
    t_bill = []
    EC_avg =[]
    Total = 0
    ec_avg = 0
    EC_N = EC_N
    EC_P = EC_P
    EC_OP = EC_OP
    # fixed_charge_m = fixed_charge_m
    # print(fixed_charge_m)
    for j in range (0,12):
        m_units = month_units[j] * (1 + (n * load_esc))
        m_units_n = month_units_n[j] * (1 + (n * load_esc))
        m_units_p = month_units_p[j] * (1 + (n * load_esc))
        m_units_op = month_units_op[j] * (1 + (n * load_esc))
        # print(m_units)
        # print(m_units_n)
        # print(m_units_p)
        # print(m_units_op)
        list_m = [m_units, m_units_n, m_units_p, m_units_op, n, EC_N, EC_P, EC_OP]
        #     # Variable for 25 year analysis
        FC = fixed_charge_m * (1 + (n * cost_esc))
        # print(FC)
        EC_T = EC(list_m)
        EC_t = EC_T[0]
        # ec_avg = EC_T[1]
        # print(EC_t)


        Total: int = FC + EC_t
        # print('BAU bill:', n, j, EC_t)
        t_bill.append(Total)
        EC_avg.append((EC_t))
        # print(t_bill)
        # end time
        end = time.time()

        runtime = (end - start)
        print('The runtime Bill without system inside:', runtime)

    return t_bill, EC_avg

# print(bill_w_o_sys(0))

