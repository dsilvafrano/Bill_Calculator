#TOU and tiered calculation of energy charge
import time
# starting time
start = time.time()

import pandas as pd
import numpy as np

import Inputs
import SQL
import Monthly
import Monthwise
import API
import TOU
import FC_EC_calc
from escalation import slab_selection
from power_balance25 import esc25
from unit_w_sys25 import unit_w_sys25
from grid_w_sys25 import grid_w_sys25
from SQL import network_charge_fetch
#SQL connection
conn = SQL.conn

# Inputs required
x1 = np.zeros(2, dtype=float)
x1[0] = Inputs.x1[0] # user input solar capacity
x1[1] = Inputs.x1[1] # user input storage capacity
load_esc = SQL.load_esc
cost_esc = SQL.cost_esc
tou_select = SQL.tou_select
# print(tou_select)
# TOU matrix
TOU = TOU.tou_matrix

def EC(list):
    # # starting time
    # start1 = time.time()
    for j in range (0,12):
        m_units = list[0]
        m_units_n = list[1]
        m_units_p = list[2]
        m_units_op = list[3]
        n = list[4]

        bill_amt_EC = 0
        bill_amt_n = 0
        bill_amt_p = 0
        bill_amt_op = 0
        list_s = [m_units, n]
        EC_s = slab_selection(list_s)
        EC = EC_s[0]
        EC_p = EC_s[2]
        EC_op = EC_s[3]
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


        bill_amt_EC = int(bill_amt_n + bill_amt_p + bill_amt_op)
        # end time
        # end1 = time.time()
        #
        # runtime1 = (end1 - start1)
        # print('The runtime EC charge selection:', runtime1)
        return bill_amt_EC

# print(EC(1000, 600, 200, 200, 1))
# end time
end = time.time()

runtime = (end - start)
print('The runtime EC bill:', runtime)