# To generate SOC for a year
import time

# starting time
# start = time.time()
#Packages required
from Inputs import x1, socin, socmax, batstatus
from SQL import socmin
import numpy as np

n = 8760
batstatus = batstatus[0]
# x1 = np.zeros(2, dtype=float)
# x1[0] = Inputs.x1[0] # user input solar capacity
# x1[1] = Inputs.x1[1] # user input storage capacity
bat_inv = 0.835 * x1[0]
socbatmax = socmax * x1[1]
# print('SOC max', socbatmax)
socbatmin = socmin * x1[1]
# print('SOC min', socbatmin)
socin = socin * x1[1]

# print(batstatus)
ch_dis_available = np.zeros(n)

def SOC(ch_dis_available):
	soc = np.zeros(n)
	soc[0] = socin
	battery_power = np.zeros(n)

	for i in range(n - 1):
		k = i + 1
		if batstatus[k] == -1:
			if (ch_dis_available[k] + soc[k - 1]) < socbatmax:
				soc[k] = ch_dis_available[k] + soc[k - 1]
			else:
				soc[k] = socbatmax
		if batstatus[k] == 1:
			if (soc[k - 1] - ch_dis_available[k]) > socbatmin:
				soc[k] = soc[k - 1] - ch_dis_available[k]
			else:
				soc[k] = socbatmin
		elif batstatus[k] == 0:
			soc[k] = soc[k - 1]

		battery_power[k] = soc[k - 1] - soc[k]  # calculating actual battery discharging and charging power
	# print(soc)
	return battery_power


# end time
# end = time.time()
# runtime = (end - start)
# print('The runtime for SOC is:', runtime)
