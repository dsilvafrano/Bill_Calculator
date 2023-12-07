###25 year economic analysis for rooftop solar with or without battery
##The file contains inputs required and API call to find solar output for specified location

##Packages required
import numpy as np
import pandas as pd

#
# # starting time
# start = time.time()

#Inputs from users
latitude = 12.0052#19.076090#23.486839#26.850000 #12.0052 #23.033863 #9.894568695410525 #12.0052
longitude = 79.8089#72.877426#75.659157#80.949997 #79.8089 #72.585022 #78.07983441534354 #79.8069
sload = 10  # from user
tariff_id = 1 # consumer type Domestic=1, Industrial=2, Commercial=3, Private=4, Public=5,
                # Domestic-LT1-D = 6, E.V charging = 7, Group Housing Society = 8
voltage_id = 1 # voltage type LT = 1, HT = 2
voltage = "LT"
tariff = 'Domestic' #Domestic, Industrial, Commercial, Private, Public,Domestic-LT1-D, E.V charging, Group Housing Society
residence_type = 'Independent House'
metering_id = 1
state_id = 1
state = "Tamil Nadu"#"Maharashtra"#"Madhya Pradesh"#"Uttar Pradesh" #"Gujarat" #"Delhi" #"Tamil Nadu"
metering_type = "Net Feed In" #Gross Metering, Net Feed In, Net Metering
weekend_consumption_change = -0.25
weekend_consumption_separate = 1 # if this is 1, it means there is weekend consumption
load_input_type = "average_monthly"# monthwise & average_monthly
# month_wise & average_monthly
avg_monthly = 250
# in case of monthwise load_input_type
mc1 = 250
mc2 = 250
mc3 = 250
mc4 = 250
mc5 = 250
mc6 = 250
mc7 = 250
mc8 = 250
mc9 = 250
mc10 = 250
mc11 = 250
mc12 = 250

# Define load distribution for 24hrs weekday
# weekday_consumption_6to10 = 30
# weekday_consumption_10to18 = 10
# weekday_consumption_18to22 = 40
# weekday_consumption_22to6 = 20

weekday_consumption_5to9 = 20
weekday_consumption_9to17 = 50
weekday_consumption_17to22 = 20
weekday_consumption_22to5 = 10

# Define load distribution for 24hrs weekend


# weekend_consumption_6to10 = 20
# weekend_consumption_10to18 = 40
# weekend_consumption_18to22 = 30
# weekend_consumption_22to6 = 10

weekend_consumption_5to9 = 20
weekend_consumption_9to17 = 50
weekend_consumption_17to22 = 20
weekend_consumption_22to5 = 10

# tou_select = 0
nyr = 26
solar = True
battery = True
x1 = np.zeros(2, dtype=float)
x1[0] = 1 # user input solar capacity
x1[1] = 1# user input storage capacity
# print(x1[0])
der_deg = 0.01  # solar degradation
bat_type = 1  # battery type = 1 fo Li ion, 0 for lead acid
socin = 0.2
socmax = 0.9

#Ma
batstatus = pd.read_csv("dispatch_strategy(Teddy).csv", header=None)  # need to be replaced with the actual dispatch strategy
# print(batstatus[24:48])

solarpv_subsidy = 0 #14588, 11670.4, 10420, 9725.33

ts = pd.date_range(start='2022-01-01', periods=8760, freq='1h')
wk = ts.day_name()

# def tou():
#     #tou selection for case
#     conn = SQL.create_connection()
#     tou_select_q = pd.read_sql_query("select applicability_periods from tou_applicability_periods where state_id=" + str(
#                     state_id) + " and tariff_type_id=" + str(tariff_id) + " and voltage_type_id=" + str(voltage_id), conn)
#     tou_select = int(tou_select_q.values[0])
#     # print('TOU',tou_select)
#     return tou_select
# print(solarp[0:24])


# end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime API:', runtime)


