###25 year economic analysis for rooftop solar with or without battery
##The file contains inputs required and API call to find solar output for specified location

##Packages required
import numpy as np
import pandas as pd

#
# # starting time
# start = time.time()

#Inputs from users
latitude = 9.894568695410525
longitude = 78.07983441534354
sload = 9 # from user
tariff_id = 1 # consumer type
voltage_id = 1 # voltage type
voltage = "LT"
tariff = 'Domestic' #Domestic, Industrial, Commercial, Private, Public
residence_type = 'Independent House'
metering_id = 7
state_id = 1
state = "Tamil Nadu"
metering_type = "Net Metering" #Gross Metering, Net Feed In, Net Metering
weekend_consumption_change = 0.5
weekend_consumption_separate = 1 # if this is 1, it means there is weekend consumption
load_input_type = "average_monthly"# monthwise & average_monthly
# month_wise & average_monthly
avg_monthly = 210
# in case of monthwise load_input_type
mc1 = 8535
mc2 = 8551
mc3 = 8444
mc4 = 10483
mc5 = 6810
mc6 = 6763
mc7 = 9963
mc8 = 10540
mc9 = 11310
mc10 = 11174
mc11 = 8184
mc12 = 7407

# Define load distribution for 24hrs weekday
weekday_consumption_6to10 = 20
weekday_consumption_10to18 = 50
weekday_consumption_18to22 = 20
weekday_consumption_22to6 = 10


# Define load distribution for 24hrs weekend


weekend_consumption_6to10 = 20
weekend_consumption_10to18 = 50
weekend_consumption_18to22 = 20
weekend_consumption_22to6 = 10

# tou_select = 0
nyr = 26
solar = True
battery = False
# x1 = np.zeros(2, dtype=float)
# x1[0] = 9.82 # user input solar capacity
# x1[1] = 1.28 # user input storage capacity
# print(x1[0])
der_deg = 0.01  # solar degradation
bat_type = 1  # battery type = 1 fo Li ion, 0 for lead acid
socin = 0.2
socmax = 0.9

#Ma
batstatus = pd.read_csv("dispatch_strategy(Teddy).csv", header=None)  # need to be replaced with the actual dispatch strategy
# print(batstatus[24:48])

solarpv_subsidy = 0

ts = pd.date_range(start='2022-01-01', periods=8760, freq='1h')
wk = ts.day_name()
# print(solarp[0:24])
# end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime API:', runtime)


