#Running function to check run time
# Packages required
import time
# starting time
start = time.time()

from line_profiler import LineProfiler
from power_balance25 import esc25

# starting time
start1 = time.time()
# def function():
#
#     n = financial_calc([10,1])
#     return n

profiler = LineProfiler()
profiler.add_function(esc25)

# Run the profiler
profiler.runcall(esc25, [10,1])

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