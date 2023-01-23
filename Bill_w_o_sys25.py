# 25 year bill without system calculation

# Packages required
import time
# starting time
# start = time.time()

import pandas as pd
# import Bill_w_o_sys
from Bill_w_o_sys import bill_w_o_sys

# 25 year bill without system
def bill_w_o_sys25():
    # starting time
    # start2 = time.time()
    bill_w_o_sys25 = pd.DataFrame()
    bill_w_o_sys25_t = 0
    bill_w_o_sys25_T = []
    for i in range(0,26):
        # starting time
        start = time.time()
        bill_w_o_sys25_t = (bill_w_o_sys(i))
        bill_w_o_sys25_T = bill_w_o_sys25_t
        bill_w_o_sys25['year' + str(i)] = bill_w_o_sys25_T
    # print(bill_w_o_sys25)
    # end time
    # end2 = time.time()
    #
    # runtime2 = (end2 - start2)
    # print('The runtime Bill without system:',i,':', runtime2)
    # bill_w_o_sys25['Total'] = bill_w_o_sys25_T

    return bill_w_o_sys25
# starting time
# start1 = time.time()

# bill_w_o_sys25 = (bill_w_o_sys25())
# print('The 25 year bill is:', (bill_w_o_sys25))

# end time
# end1 = time.time()
#
# runtime1 = (end1 - start1)
# print('The runtime Bill without system : print:', runtime1)

# end time
# end = time.time()
#
# runtime = (end - start)
# # print('The runtime Bill without system 25 year:', runtime)