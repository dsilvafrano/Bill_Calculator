## Building an hourly load profile from monthly average data
import time

# starting time
# start = time.time()

# Packages required
import pandas as pd
import numpy as np
from Inputs import wk, ts, avg_monthly, weekend_consumption_separate, weekend_consumption_change,\
    weekday_consumption_6to10,weekday_consumption_10to18,weekday_consumption_18to22,weekday_consumption_22to6,\
    weekend_consumption_6to10,weekend_consumption_10to18,weekend_consumption_22to6,weekend_consumption_18to22
from TOU import tou_matrix



# print('Entering monthly')

# In case of monthly average
avg_monthly = avg_monthly
TOU = tou_matrix
# print(avg_monthly)

# Retrieving dataframe with time stamp and days
days = wk
TS = ts

# print(TS[0:24])
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


# Building an empty a dataframe to store hourly values
user_load_n = np.array(([0] * 24), dtype=float)

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

#In the case the weekend_consumption_separate == 0
if int(weekend_consumption_separate) == 0:
    user_load_n[6:10] = round((weekday_consumption_6to10n * avg_monthly * 12 / (365 * 4)), 3)
    user_load_n[10:18] = round((weekday_consumption_10to18n * avg_monthly * 12 / (365 * 8)), 3)
    user_load_n[18:22] = round((weekday_consumption_18to22n * avg_monthly * 12 / (365 * 4)), 3)
    user_load_n[22:24] = round((weekday_consumption_22to6n * avg_monthly * 12 * 0.25 / (365 * 2)), 3)
    user_load_n[0:6] = round((weekday_consumption_22to6n * avg_monthly * 12 * 0.75 / (365 * 6)), 3)

# Applying the daily consumption to the whole year
    user_load_n = np.tile(user_load_n, 365)

    # print(sum(user_load)/12)
else:
    weekday_24 = np.array(([0] * 24), dtype=float)
    weekend_24 = np.array(([0] * 24), dtype=float)

    weekday_daily = round((avg_monthly * 12) / (261 + round(104 * (weekend_consumption_change + 1))))
    weekend_daily = round((weekend_consumption_change + 1) * weekday_daily)

    weekday_24[6:10] = round((weekday_consumption_6to10n * (weekday_daily) / 4), 3)
    weekday_24[10:18] = round((weekday_consumption_10to18n * (weekday_daily) / 8), 3)
    weekday_24[18:22] = round((weekday_consumption_18to22n * (weekday_daily) / 4), 3)
    weekday_24[22:24] = round((weekday_consumption_22to6n * (weekday_daily * 0.25) / 2), 3)
    weekday_24[0:6] = round((weekday_consumption_22to6n * (weekday_daily * 0.75) / 6), 3)

    weekend_24[6:10] = round((weekend_consumption_6to10n * (weekend_daily) / 4), 3)
    weekend_24[10:18] = round((weekend_consumption_10to18n * (weekend_daily) / 8), 3)
    weekend_24[18:22] = round((weekend_consumption_18to22n * (weekend_daily) / 4), 3)
    weekend_24[22:24] = round((weekend_consumption_22to6n * (weekend_daily * 0.25) / 2), 3)
    weekend_24[0:6] = round((weekend_consumption_22to6n * (weekend_daily * 0.75) / 6), 3)

    df_load = []

    for i in range(365):
        if days[i * 24] == 'Saturday' or days[i * 24] == 'Sunday':
            df_load.extend(weekend_24)
        else:
            df_load.extend(weekday_24)

    user_load_n = df_load
    # print('Monthly',sum(df_load))
# date = date.today()
# year = date.year
# days_n =366 if calendar.isleap(year) else 365

user_load = pd.DataFrame()
avg_in_month = []
user_load['date&time'] = TS
user_load['Load'] = user_load_n
# cumulated for every hour of the month
user_load['cumulative'] = user_load.groupby((user_load['date&time']).dt.month)['Load'].cumsum()
user_load['TOU'] = TOU
# cumulated for every hour of the month
# user_load['cumulative'] = user_load.groupby((user_load['date&time']).dt.month)['Load'].cumsum()
# user_load['cumulative_TOU'] = user_load.groupby((user_load['TOU']))['Load'].cumsum()
user_load['normal'] = np.where(user_load['TOU'] == 1, user_load['Load'], 0)
# user_load['cumulative_N'] = user_load.groupby((user_load['date&time']).dt.month)['normal'].cumsum()
user_load['peak'] = np.where(user_load['TOU'] == 2, user_load['Load'], 0)
# user_load['cumulative_P'] = user_load.groupby((user_load['date&time']).dt.month)['peak'].cumsum()
user_load['offpeak'] = np.where(user_load['TOU'] == 3, user_load['Load'], 0)
# user_load['cumulative_OP'] = user_load.groupby((user_load['date&time']).dt.month)['offpeak'].cumsum()

# # data re-sampled based on each month(gives 12 values with sum for each month)
avg_in_month = user_load.resample('MS', on='date&time').Load.sum()
avg_in_month_n = user_load.resample('MS', on='date&time').normal.sum()
avg_in_month_p = user_load.resample('MS', on='date&time').peak.sum()
avg_in_month_op = user_load.resample('MS', on='date&time').offpeak.sum()
# print((user_load[0:24]))
# print(avg_in_month, avg_in_month_n, avg_in_month_p, avg_in_month_op)
# print(avg_in_month)


# print(days)

# # Build a list of number of days in a month
# days_in_month = []
# for i in range(1, 13):
#     d_month = monthrange(year, i)[1]
#     days_in_month.append(d_month)
# # print(len(days_in_month))
#
# # Build a matrix for average monthly of each month
# d_avg = sum(user_load['Load'])/days_n
# avg_in_month = [i * d_avg for i in days_in_month]

# print((avg_in_month))
# end time
# end = time.time()
#
# runtime = (end - start)
# print('The runtime Monthly:', runtime)

