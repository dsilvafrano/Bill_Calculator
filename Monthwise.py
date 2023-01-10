## Building an hourly load profile from monthwise data
import calendar
import time

# starting time
start = time.time()

# Packages required
import pandas as pd
import numpy as np
from calendar import monthrange
from Inputs import wk,ts,weekend_consumption_separate, weekend_consumption_change,\
    weekday_consumption_6to10,weekday_consumption_10to18,weekday_consumption_18to22,weekday_consumption_22to6,\
    weekend_consumption_6to10,weekend_consumption_10to18,weekend_consumption_22to6,weekend_consumption_18to22,mc1,mc2,\
    mc3,mc4,mc5,mc6,mc7,mc8,mc9,mc10,mc11,mc12
from TOU import tou_matrix
import datetime

# print('Entering monthwise')

# In case of monthwise
monthwise = [mc1, mc2, mc3, mc4, mc5, mc6, mc7, mc8, mc9, mc10, mc11, mc12]
TOU = tou_matrix
# print(monthwise)

# Retrieving dataframe with time stamp and days
days = wk
TS = ts
# print(days[0:24])
# Define weekend consumption
weekend_consumption_separate = weekend_consumption_separate
weekend_consumption_change = weekend_consumption_change

# Weekday consumption
weekday_consumption_6to10 = weekday_consumption_6to10
weekday_consumption_10to18 = weekday_consumption_10to18
weekday_consumption_18to22 = weekday_consumption_18to22
weekday_consumption_22to6 = weekday_consumption_22to6
# print(weekday_consumption_22to6)

# Weekend consumption
weekend_consumption_6to10 = weekend_consumption_6to10
weekend_consumption_10to18 = weekend_consumption_10to18
weekend_consumption_18to22 = weekend_consumption_18to22
weekend_consumption_22to6 = weekend_consumption_22to6
# print(weekend_consumption_22to6)


# Determining the percentage share of weekday and weekend

weekday_consumption_6to10n = weekday_consumption_6to10 / ((
                weekday_consumption_6to10 + weekday_consumption_10to18 + weekday_consumption_18to22 + weekday_consumption_22to6))
weekday_consumption_10to18n = weekday_consumption_10to18 / ((
                weekday_consumption_6to10 + weekday_consumption_10to18 + weekday_consumption_18to22 + weekday_consumption_22to6))
weekday_consumption_18to22n = weekday_consumption_18to22 / ((
                weekday_consumption_6to10 + weekday_consumption_10to18 + weekday_consumption_18to22 + weekday_consumption_22to6))
weekday_consumption_22to6n = weekday_consumption_22to6 / ((
                weekday_consumption_6to10 + weekday_consumption_10to18 + weekday_consumption_18to22 + weekday_consumption_22to6))

# print(weekday_consumption_22to6n)

# In case the user specifies the weekend consumption and allocated percentage

if int(weekend_consumption_separate) == 1:
    weekend_consumption_6to10n = weekend_consumption_6to10 / ((
            weekend_consumption_6to10 + weekend_consumption_10to18 + weekend_consumption_18to22 + weekend_consumption_22to6))
    weekend_consumption_10to18n = weekend_consumption_10to18 / ((
            weekend_consumption_6to10 + weekend_consumption_10to18 + weekend_consumption_18to22 + weekend_consumption_22to6))
    weekend_consumption_18to22n = weekend_consumption_18to22 / ((
            weekend_consumption_6to10 + weekend_consumption_10to18 + weekend_consumption_18to22 + weekend_consumption_22to6))
    weekend_consumption_22to6n = weekend_consumption_22to6 / ((
            weekend_consumption_6to10 + weekend_consumption_10to18 + weekend_consumption_18to22 + weekend_consumption_22to6))

# print(weekend_consumption_22to6n)

# Build a list of number of days in a month
days_in_month = []
for i in range(1, 13):
    d_month = monthrange(2022, i)[1]
    days_in_month.append(d_month)

# print(days_in_month)


#In the case the weekend_consumption_separate == 0
if int(weekend_consumption_separate) == 0:
    # Building an empty a list to store hourly values
    user_load_n = []
    for i in range(0, 12):
        user_load_t = np.array(([0]*24), dtype=float)
        # print(len(user_load_t))
        user_load_t[6:10] = round((weekday_consumption_6to10n * monthwise[i] / (days_in_month[i] * 4)), 3)
        user_load_t[10:18] = round((weekday_consumption_10to18n * monthwise[i] / (days_in_month[i] * 8)), 3)
        user_load_t[18:22] = round((weekday_consumption_18to22n * monthwise[i] / (days_in_month[i] * 4)), 3)
        user_load_t[22:24] = round((weekday_consumption_22to6n * monthwise[i] * 0.25 / (days_in_month[i] * 2)), 3)
        user_load_t[0:6] = round((weekday_consumption_22to6n * monthwise[i] * 0.75 / (days_in_month[i] * 6)), 3)

        user_load_t = np.tile(user_load_t, days_in_month[i])
        # print(len(user_load_t))
        user_load_n.extend(user_load_t)
    # print(sum(user_load_n)/12)

else:
    # Building an empty a list to store hourly values
    user_load_n = []
    avg_in_month = []
    # Determining weekday and weekend consumption from monthwise
    for i in range(0, 12):
        start_date = datetime.date(2022, i+1, 1)
        end_date = datetime.date(2022, i+1, days_in_month[i])
        # print(start_date)
        # print(end_date)
        num_weekday = np.busday_count(start_date,end_date)
        num_weekend = days_in_month[i] - num_weekday
        # print(num_weekday)
        # print(num_weekend)
        weekday_t = round(monthwise[i] / ((num_weekday) + round((num_weekend * (weekend_consumption_change + 1)))),1)
        weekend_t = round(((weekend_consumption_change + 1) * weekday_t),1)
        # print(weekday_t)
        # print(weekend_t)

        weekday_24 = np.array(([0] * 24), dtype=float)
        weekend_24 = np.array(([0] * 24), dtype=float)

        weekday_24[6:10] = round((weekday_consumption_6to10n * weekday_t / 4),2)
        weekday_24[10:18] = round((weekday_consumption_10to18n * weekday_t / 8),2)
        weekday_24[18:22] = round((weekday_consumption_18to22n * weekday_t / 4),2)
        weekday_24[22:24] = round((weekday_consumption_22to6n * weekday_t * 0.25 / 2),2)
        weekday_24[0:6] = round((weekday_consumption_22to6n * weekday_t * 0.75 / 6),2)

        weekend_24[6:10] = round((weekend_consumption_6to10n * weekend_t / 4),2)
        weekend_24[10:18] = round((weekend_consumption_10to18n * weekend_t / 8),2)
        weekend_24[18:22] = round((weekend_consumption_18to22n * weekend_t / 4),2)
        weekend_24[22:24] = round((weekend_consumption_22to6n * weekend_t * 0.25 / 2),2)
        weekend_24[0:6] = round((weekend_consumption_22to6n * weekend_t * 0.75 / 6),2)

        # print(weekday_24)
        # print(weekend_24)

        df_load = []


        for i in range(0,days_in_month[i]):
            if days[i * 24] == 'Saturday' or days[i * 24] == 'Sunday':
                df_load.extend(weekend_24)
            else:
                df_load.extend(weekday_24)
            # a = float(sum(df_load))
        # print(a)
        user_load_n.extend(df_load)
        # avg_in_month.append(a)
# print(sum(user_load_n)/12)
# print(avg_in_month)

# date = date.today()
# year = date.year
# days=366 if calendar.isleap(year) else 365

user_load = pd.DataFrame()
avg_in_month = []
user_load['date&time'] = TS
user_load['Load'] = user_load_n
user_load['TOU'] = TOU
# cumulated for every hour of the month
# user_load['cumulative'] = user_load.groupby((user_load['date&time']).dt.month)['Load'].cumsum()
# user_load['cumulative_TOU'] = user_load.groupby((user_load['TOU']))['Load'].cumsum()
user_load['normal'] = np.where(user_load['TOU'] == 1, user_load['Load'], 0)
user_load['cumulative_N'] = user_load.groupby((user_load['date&time']).dt.month)['normal'].cumsum()
user_load['peak'] = np.where(user_load['TOU'] == 2, user_load['Load'], 0)
user_load['cumulative_P'] = user_load.groupby((user_load['date&time']).dt.month)['peak'].cumsum()
user_load['offpeak'] = np.where(user_load['TOU'] == 3, user_load['Load'], 0)
user_load['cumulative_OP'] = user_load.groupby((user_load['date&time']).dt.month)['offpeak'].cumsum()

# # data re-sampled based on each month(gives 12 values with sum for each month)
avg_in_month = user_load.resample('MS', on='date&time').Load.sum()
avg_in_month_n = user_load.resample('MS', on='date&time').normal.sum()
avg_in_month_p = user_load.resample('MS', on='date&time').peak.sum()
avg_in_month_op = user_load.resample('MS', on='date&time').offpeak.sum()
# print((user_load[0:24]))
# print(avg_in_month, avg_in_month_n, avg_in_month_p, avg_in_month_op)
# print(avg_in_month_n)
# print(avg_in_month_p)
# print(avg_in_month_op)
# print(bill_units)

# end time
end = time.time()

runtime = (end - start)
print('The runtime Monthwise:', runtime)


