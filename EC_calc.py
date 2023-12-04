#TOU and tiered calculation of energy charge
import time
# starting time
# start = time.time()

from SQL import tou_select
from escalation import slab_selection
import numpy as np

# Inputs required
tou_select = tou_select
# print(tou_select)


def EC(list):
    # # starting time
    # start1 = time.time()
    EC_N = list[5]
    EC_P = list[6]
    EC_OP = list[7]
    for j in range (0,12):
        m_units = list[0]
        m_units_n = list[1]
        m_units_p = list[2]
        m_units_op = list[3]
        n = list[4]

        bill_amt_EC = 0
        Ec_avg = 0
        bill_amt_n = 0
        bill_amt_p = 0
        bill_amt_op = 0
        list_s = [m_units, n, EC_N, EC_P, EC_OP]
        if m_units == 0:
            bill_amt_n = 0
            bill_amt_p = 0
            bill_amt_op = 0
        else:

            # print(list_s)
            EC_s = slab_selection(list_s)
            EC = EC_s[0]
            Ec_avg = np.mean(EC['energy_charge'])
            # Ec_avg = EC['energy_charge'].mean()
            EC_p = EC_s[2]
            EC_op = EC_s[3]
            # EC['energy_charge'] * (1 + (n * cost_esc))
            # print(EC)
            # EC_p['energy_charge'] * (1 + (n * cost_esc))
            # print(EC['energy_charge'])
            # EC_op['energy_charge'] * (1 + (n * cost_esc))
            # print(EC_op['energy_charge'])
            # print(EC_s)
            m_tier = EC['tier'].max()
            # print(m_tier)
            # print(EC['bill_amt'])
            # print(EC['energy_charge'])
            for i in range(1,(m_tier+1)):
                if m_units_n >= (EC['maximum'][i-1] - EC['min'][i-1]):
                    # print('in')
                    bill_amt_n = int(bill_amt_n + EC['bill_amt'][i-1])
                    m_units_n = m_units_n - (EC['maximum'][i-1] - EC['min'][i-1])
                else:
                    bill_amt_n = int(bill_amt_n + (m_units_n * EC['energy_charge'][i - 1]))
                    break
                # print('bil amt:', bill_amt_n)
                # print('units:',m_units_n)
                # print('Normal, Peak, Of-peak', m_units_n * EC['energy_charge'][i - 1],
                #       m_units_p * EC_p['energy_charge'][i - 1],
                #       m_units_op * EC_op['energy_charge'][i - 1])
            for i in range(1, (m_tier + 1)):
                if tou_select == 1 or tou_select == 2:  # 1 means applicable and 2 means optional
                    if m_units_p >= (EC_p['maximum'][i - 1] - EC_p['min'][i - 1]):
                        bill_amt_p = int(bill_amt_p + EC_p['bill_amt'][i - 1])
                        m_units_p = m_units_p - (EC_p['maximum'][i - 1] - EC_p['min'][i - 1])
                    else:
                        bill_amt_p = int(bill_amt_p + (m_units_p * EC_p['energy_charge'][i - 1]))
                        break
                else:
                    bill_amt_p = 0

            for i in range(1, (m_tier + 1)):
                if tou_select == 1 or tou_select == 2:  # 1 means applicable and 2 means optional
                    if m_units_op >= (EC_op['maximum'][i - 1] - EC_op['min'][i - 1]):
                        bill_amt_op = int(bill_amt_op + EC_op['bill_amt'][i - 1])
                        m_units_op = m_units_op - (EC_op['maximum'][i - 1] - EC_op['min'][i - 1])
                    else:
                        bill_amt_op = int(bill_amt_op + (m_units_op * EC_op['energy_charge'][i - 1]))
                        break
                        # print(bill_amt)
                else:
                    bill_amt_p = 0
                    bill_amt_op = 0

        # print('Normal, Peak, Of-peak', bill_amt_n, bill_amt_p, bill_amt_op)
        bill_amt_EC = int(bill_amt_n + bill_amt_p + bill_amt_op)
        # print('normal', bill_amt_n)
        # print('peak', bill_amt_p)
        # print('off-peak', bill_amt_op)
        # end time
        # end1 = time.time()
        #
        # runtime1 = (end1 - start1)
        # print('The runtime EC charge selection:', runtime1)
        return bill_amt_EC, Ec_avg

# list  =[103.042, 103.042, 0, 0, 0]
# print(EC(list))
# end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime EC bill:', runtime)