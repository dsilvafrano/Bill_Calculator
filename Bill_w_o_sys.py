# Calculate the monthly bill without system

# Packages required
import time
# starting time
# start = time.time()

import pandas as pd

from Inputs import load_input_type
from SQL import conn, load_esc, cost_esc, tou_select
from Monthly import avg_in_month, avg_in_month_n, avg_in_month_p, avg_in_month_op
# using 'from monthwise' results in same variable, giving incorrect results, hence retained the below call method
import Monthwise
from FC_EC_calc import fixed_charge_m
from EC_calc import EC

# Function to do the bill calculation
def bill_w_o_sys(n):
    if load_input_type == "average_monthly":
        month_units = avg_in_month
        month_units_n = avg_in_month_n
        month_units_p = avg_in_month_p
        month_units_op = avg_in_month_op
        # print('Units', month_units)
    else:
        month_units = Monthwise.avg_in_month
        month_units_n = Monthwise.avg_in_month_n
        month_units_p = Monthwise.avg_in_month_p
        month_units_op = Monthwise.avg_in_month_op
        # print('Units', month_units)


    # m_units = 1000
    t_bill = []
    Total = 0
    # fixed_charge_m = fixed_charge_m
    # print(fixed_charge_m)
    for j in range (0,12):
        m_units = month_units[j] * (1 + (n * load_esc))
        m_units_n = month_units_n[j] * (1 + (n * load_esc))
        m_units_p = month_units_p[j] * (1 + (n * load_esc))
        m_units_op = month_units_op[j] * (1 + (n * load_esc))
        # print(m_units_n)
        list_m = [m_units, m_units_n, m_units_p, m_units_op, n]
        #     # Variable for 25 year analysis
        FC = fixed_charge_m * (1 + (n * cost_esc))
        # print(FC)
        EC_t = EC(list_m)
        # print(EC_t)


        Total: int = FC + EC_t
        t_bill.append(Total)
        # print(t_bill)

    return t_bill

# print(bill_w_o_sys(0))

# end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime Bill without system inside:', runtime)