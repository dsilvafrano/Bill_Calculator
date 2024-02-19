# To generate SOC for a year
import time

# starting time

#Packages required
from Inputs import socin, socmax, batstatus
from SQL import socmin
import numpy as np

n = 8760
batstatus = batstatus[0]
# x1 = np.zeros(2, dtype=float)
# x1[0] = Inputs.x1[0] # user input solar capacity
# x1[1] = Inputs.x1[1] # user input storage capacity


# print(batstatus)
ch_dis_available = np.zeros(n)

def SOC(ch_dis_available, x1):
	start = time.time()
	bat_inv = 0.835 * x1[0]
	socbatmax = socmax * x1[1]
	# print('SOC max', socbatmax)
	socbatmin = socmin * x1[1]
	# print('SOC min', socbatmin)
	socbatin = socin * x1[1]
	soc = np.zeros(n)
	soc[0] = socbatin
	# soc = np.array(([0.2] * 8760), dtype=float)
	# battery_power = np.zeros(n)
	batt = np.empty(n)
	batt[0] = 0

	soc_old = 0
	# soc_new = 0

	# for i in range(n - 1):
	# 	k = i + 1
	# 	if batstatus[k] == -1 and (ch_dis_available[k] + soc[k - 1]) < socbatmax:
	# 		soc[k] = ch_dis_available[k] + soc[k - 1]
	# 	else:
	# 		soc[k] = socbatmax
	# 	if batstatus[k] == 1 and (soc[k - 1] - ch_dis_available[k]) > socbatmin:
	# 		soc[k] = soc[k - 1] - ch_dis_available[k]
	# 	else:
	# 		soc[k] = socbatmin
	# 	if batstatus[k] == 0:
	# 		soc[k] = soc[k - 1]
	#
	# 	battery_power[k] = soc[k - 1] - soc[k]  # calculating actual battery discharging and charging power
	for k in range(1, n):
		soc_old = soc[k-1]
		# print(soc)
		if batstatus[k] == -1:
			soc[k] = min(ch_dis_available[k] + soc_old, socbatmax)
		elif batstatus[k] == 1:
			soc[k] = max(soc_old - ch_dis_available[k], socbatmin)
		else:
			soc[k] = soc_old
		# soc[k] = min(ch_dis_available[k] + soc[k - 1], socbatmax) if batstatus[k] == -1 \
		# 	else max(soc[k - 1] - ch_dis_available[k], socbatmin) if batstatus[k] == 1 else soc[k - 1]
		# soc[k] = soc_new
		# soc = np.array(([0.2] * 8760), dtype=float)
	# soc = np.where((batstatus == 1), max(soc[:-1] - ch_dis_available[1:], socbatmin),
	# 			   np.where((batstatus == -1),min(ch_dis_available[1:] + soc[:-1],socbatmax),soc[:-1]))
		# soc = np.where(batstatus == -1,min(ch_dis_available[k] + soc[k-1], socbatmax),soc[k])


	# battery_power = soc[]
	# battery_power[k] = soc[k - 1] - soc[k]
	# 	battery_power[k] = soc[k - 1] - soc[k]
	soc_n = soc[:-1]
	soc_n1 = soc[1:]
	batt[1:] = soc_n - soc_n1
	battery_power = np.where(batt < 0, 0, batt)
	# print('SOC',soc[0:24])
	# print('bat_sta',batstatus[0:24])
	# print('Charge_Dis',ch_dis_available[0:24])
	# print((soc_n[0:24]))
	# print(((soc_n1[0:24])))
	# print(batt[0:24].round(3))
	end = time.time()
	runtime = (end - start)
	print('The runtime for SOC is:', runtime)
	return battery_power
#
# soc = np.zeros((8760))
# for k in range(0,26):
# 	print(k)
# 	Soc = SOC(np.zeros(8760),[1,1]).round(3)
# print(Soc[0:24])
# end time


