# 25 year bill without system calculation

# Packages required
import time
# starting time


import pandas as pd
# import Bill_w_o_sys
from EC_select import EC_select
from Bill_w_o_sys import bill_w_o_sys

# 25 year bill without system
def bill_w_o_sys25():
    start = time.time()
    # starting time
    # start2 = time.time()
    bill_w_o_sys25 = pd.DataFrame()
    EC_avg25 = pd.DataFrame()
    EC = EC_select()
    EC_N = EC[0]
    EC_P = EC[1]
    EC_OP = EC[2]
    bill_w_o_sys25_t = 0
    bill_w_o_sys25_T = []
    for i in range(0,26):
        # starting time
        start = time.time()
        bill_w_o_sys25_q = (bill_w_o_sys(i,EC_N,EC_P,EC_OP))
        bill_w_o_sys25_t = bill_w_o_sys25_q[0]
        bill_w_o_sys25_T = bill_w_o_sys25_t
        bill_w_o_sys25['year' + str(i)] = bill_w_o_sys25_T
        EC_avg25['year' + str(i)] = bill_w_o_sys25_q[1]
    # print(bill_w_o_sys25)
    # end time
    # end2 = time.time()
    #
    # runtime2 = (end2 - start2)
    # print('The runtime Bill without system:',i,':', runtime2)
    # bill_w_o_sys25['Total'] = bill_w_o_sys25_T
    # end time
    end = time.time()

    runtime = (end - start)
    print('The runtime Bill without system 25 year:', runtime)
    return bill_w_o_sys25, EC_avg25
# starting time
# start1 = time.time()

# bill_w_o_sys25 = (bill_w_o_sys25()[0])
# print('The 25 year bill is:', (bill_w_o_sys25))

# end time
# end1 = time.time()
#
# runtime1 = (end1 - start1)
# print('The runtime Bill without system : print:', runtime1)

