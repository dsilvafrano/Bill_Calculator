###25 year economic analysis for rooftop solar with or without battery
##The file contains inputs required and API call to find solar output for specified location

##Packages required
import numpy as np
import pandas as pd

#
# # starting time
# start = time.time()

#Inputs from users
latitude = 12.0052 #23.033863 #9.894568695410525 #12.0052
longitude = 79.8089 #72.585022 #78.07983441534354 #79.8069
sload = 5  # from user
tariff_id = 1 # consumer type Domestic=1, Industrial=2, Commercial=3, Private=4, Public=5,
                # Domestic-LT1-D = 6, E.V charging = 7, Group Housing Society = 8
voltage_id = 1 # voltage type LT = 1, HT = 2
voltage = "LT"
tariff = 'Domestic' #Domestic, Industrial, Commercial, Private, Public,Domestic-LT1-D, E.V charging, Group Housing Society
residence_type = 'Independent House'
metering_id = 7
state_id = 1
state = "Tamil Nadu"
metering_type = "Net Metering" #Gross Metering, Net Feed In, Net Metering
weekend_consumption_change = -0.5
weekend_consumption_separate = 1 # if this is 1, it means there is weekend consumption
load_input_type = "average_monthly"# monthwise & average_monthly
# month_wise & average_monthly
avg_monthly = 1000
# in case of monthwise load_input_type
mc1 = 2000
mc2 = 2000
mc3 = 2000
mc4 = 2000
mc5 = 2000
mc6 = 2000
mc7 = 2000
mc8 = 2000
mc9 = 2000
mc10 = 2000
mc11 = 2000
mc12 = 2000

# Define load distribution for 24hrs weekday
weekday_consumption_6to10 = 20
weekday_consumption_10to18 = 50
weekday_consumption_18to22 = 20
weekday_consumption_22to6 = 10


# Define load distribution for 24hrs weekend


weekend_consumption_6to10 = 20
weekend_consumption_10to18 = 40
weekend_consumption_18to22 = 20
weekend_consumption_22to6 = 20

# tou_select = 0
nyr = 26
solar = True
battery = False
x1 = np.zeros(2, dtype=float)
x1[0] = 5 # user input solar capacity
x1[1] = 5# user input storage capacity
# print(x1[0])
der_deg = 0.01  # solar degradation
bat_type = 0  # battery type = 1 fo Li ion, 0 for lead acid
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


