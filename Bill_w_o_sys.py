# Calculate the monthly bill without system

# Packages required
import time
# starting time
start = time.time()

import pandas as pd

import Inputs
import SQL
import Monthly
import Monthwise
import API
import FC_EC_calc
import escalation

#SQL connection
conn = SQL.conn

# Inputs required
load_esc = SQL.load_esc
cost_esc = SQL.cost_esc
tou_select = SQL.tou_select
# print(tou_select)
# Function to do the bill calculation
def bill_w_o_sys(n):
    load_input_type = Inputs.load_input_type
    if load_input_type == "average_monthly":
        month_units = Monthly.avg_in_month
        month_units_n = Monthly.avg_in_month_n
        month_units_p = Monthly.avg_in_month_p
        month_units_op = Monthly.avg_in_month_op
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
    fixed_charge_m = FC_EC_calc.fixed_charge_m
    # print(fixed_charge_m)
    for j in range (0,12):
        m_units = month_units[j] * (1 + (n * load_esc))
        m_units_n = month_units_n[j] * (1 + (n * load_esc))
        m_units_p = month_units_p[j] * (1 + (n * load_esc))
        m_units_op = month_units_op[j] * (1 + (n * load_esc))

        bill_amt = 0
        bill_amt_n = 0
        bill_amt_p = 0
        bill_amt_op = 0
        FC = fixed_charge_m * (1 + (n * cost_esc))
        EC = escalation.slab_selection(m_units, n)[0]
        EC_p = escalation.slab_selection(m_units, n)[2]
        EC_op = escalation.slab_selection(m_units, n)[3]
        EC['energy_charge'] * (1 + (n * cost_esc))
        # print(EC['energy_charge'])
        EC_p['energy_charge'] * (1 + (n * cost_esc))
        # print(EC['energy_charge'])
        EC_op['energy_charge'] * (1 + (n * cost_esc))
        # print(EC_op['energy_charge'])
        # print(EC)
        m_tier = (EC['tier'].max())
        # print(EC['maximum'])
        # print(EC['bill_amt'])
        # print(EC['energy_charge'])
        for i in range(1,(m_tier+1)):
            if m_units_n >= EC['maximum'][i-1]:
                bill_amt_n = int(bill_amt_n + EC['bill_amt'][i-1])
                m_units_n = m_units_n - (EC['maximum'][i-1] - EC['min'][i-1])
            else:
                bill_amt_n = int(bill_amt_n + (m_units_n * EC['energy_charge'][i - 1]))

            if tou_select == 1 or tou_select == 2:  # 1 means applicable and 2 means optional
                if m_units_p >= EC_p['maximum'][i - 1]:
                    bill_amt_p = int(bill_amt_p + EC_p['bill_amt'][i - 1])
                    m_units_p = m_units_p - (EC_p['maximum'][i - 1] - EC_p['min'][i - 1])
                else:
                    bill_amt_p = int(bill_amt_p + (m_units_p * EC['energy_charge'][i - 1]))

                if m_units_op >= EC_op['maximum'][i - 1]:
                    bill_amt_op = int(bill_amt_op + EC_op['bill_amt'][i - 1])
                    m_units_op = m_units_op - (EC_op['maximum'][i - 1] - EC_op['min'][i - 1])
                else:
                    bill_amt_op = int(bill_amt_op + (m_units_p * EC_op['energy_charge'][i - 1]))
                    # print(bill_amt)


        bill_amt = int(bill_amt_n + bill_amt_p + bill_amt_op)
        # print(bill_amt)
        # print('N',bill_amt_n)
        # print('P',bill_amt_p)
        # print('OP',bill_amt_op)

        Total: int = FC + bill_amt
        t_bill.append(Total)
        # print(t_bill)

    return t_bill

# end time
end = time.time()

runtime = (end - start)
# print('The runtime Bill without system inside:', runtime)