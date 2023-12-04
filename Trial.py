#Running function to check run time
# Packages required
import time
# starting time
start = time.time()
import numpy as np
from line_profiler import LineProfiler
from financial_calc import financial_calc
from Bill_w_o_sys import bill_w_o_sys
from net_metering import NM
from bill_unitsNM import bill_unitsNM
from unit_w_sys25 import unit_w_sys25
from grid_w_sys25 import grid_w_sys25
from power_balance25 import esc25
from API import api
from power_balance import power_balance
from SOC import SOC
from EC_calc import EC
from escalation import slab_selection
from EC_select import EC_select
from net_feed_in import NF

# starting time
start1 = time.time()
# def function():
#
#     n = financial_calc([10,1])
#     return n

# solarp = api()
# # Converting (Wac) to (kWac)
# solarp['AC(kW)'] = solarp['AC(kW)']/1000
soc = np.array(([0.5] * 8760), dtype=float)
# EC_t = EC_select()
# EC_N = EC_t[0]
# EC_P = EC_t[1]
# EC_OP = EC_t[2]

profiler = LineProfiler()
profiler.add_function(SOC)

# Run the profiler
profiler.runcall(SOC,soc,[1,1])

# print the results
profiler.print_stats()
# print('The result is:', n)
# print('The stat is:', profiler)


# end time
end = time.time()

runtime = (end - start)
runtime1 = (end - start1)
print('The runtime of the function is:', runtime)
print('The runtime1 of the function is:', runtime1)