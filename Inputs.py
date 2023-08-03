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
sload = 10 # from user
tariff_id = 1 # consumer type
voltage_id = 1 # voltage type
voltage = "LT"
tariff = 'Domestic' #Domestic, Industrial, Commercial, Private, Public
residence_type = 'Independent House'
metering_id =7
state_id = 1
state = "Tamil Nadu"
metering_type = "Net Metering" #Gross Metering, Net Feed In, Net Metering
weekend_consumption_change = 0.25
weekend_consumption_separate = 1 # if this is 1, it means there is weekend consumption
load_input_type = "average_monthly"# monthwise & average_monthly
# month_wise & average_monthly
avg_monthly = 600
# in case of monthwise load_input_type
mc1 = 100
mc2 = 100
mc3 = 100
mc4 = 100
mc5 = 100
mc6 = 100
mc7 = 100
mc8 = 100
mc9 = 100
mc10 = 100
mc11 = 100
mc12 = 100

# Define load distribution for 24hrs weekday
weekday_consumption_6to10 = 30
weekday_consumption_10to18 = 10
weekday_consumption_18to22 = 40
weekday_consumption_22to6 = 20


# Define load distribution for 24hrs weekend


weekend_consumption_6to10 = 20
weekend_consumption_10to18 = 40
weekend_consumption_18to22 = 30
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
bat_type = 0  # battery type = 1 fo Li ion, 0 for lead acid
socin = 0.2
socmax = 0.9

#Ma
batstatus = pd.read_csv("dispatch_strategy(Teddy).csv", header=None)  # need to be replaced with the actual dispatch strategy
# print(batstatus[24:48])

solarpv_subsidy = 1000

ts = pd.date_range(start='2022-01-01', periods=8760, freq='1h')
wk = ts.day_name()
# print(solarp[0:24])
# end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime API:', runtime)


