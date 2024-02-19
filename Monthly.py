## Building an hourly load profile from monthly average data
import time

# starting time

import os
import sys
# Packages required
import pandas as pd
import numpy as np
from TOU import tou
import Inputs
from Inputs import wk, ts, avg_monthly, weekend_consumption_separate, weekend_consumption_change,\
    weekday_consumption_5to9,weekday_consumption_9to17,weekday_consumption_17to22,weekday_consumption_22to5,\
    weekend_consumption_5to9,weekend_consumption_9to17,weekend_consumption_22to5,weekend_consumption_17to22




# print('Entering monthly')
def monthly():
    start = time.time()
    try:
        # In case of monthly average
        avg_monthly = Inputs.avg_monthly
        TOU_n = tou()
        TOU = TOU_n[0]
        # print(avg_monthly)

        # Retrieving dataframe with time stamp and days
        days = Inputs.wk
        TS = Inputs.ts

        # print(TS[0:24])
        # Define weekend consumption
        weekend_consumption_separate = Inputs.weekend_consumption_separate
        weekend_consumption_change = Inputs.weekend_consumption_change

        # Weekday consumption
        weekday_consumption_5to9 = Inputs.weekday_consumption_5to9
        weekday_consumption_9to17 = Inputs.weekday_consumption_9to17
        weekday_consumption_17to22 = Inputs.weekday_consumption_17to22
        weekday_consumption_22to5 = Inputs.weekday_consumption_22to5
        # print(weekday_consumption_22to6)

        # Weekend consumption
        weekend_consumption_5to9 = Inputs.weekend_consumption_5to9
        weekend_consumption_9to17 = Inputs.weekend_consumption_9to17
        weekend_consumption_17to22 = Inputs.weekend_consumption_17to22
        weekend_consumption_22to5 = Inputs.weekend_consumption_22to5
        # print(weekend_consumption_22to6)


        # Building an empty a dataframe to store hourly values
        avg_user_load_n = np.array(([0] * 24), dtype=float)

        # Determining the percentage share of weekday and weekend

        weekday_consumption_5to9n = weekday_consumption_5to9 / ((
                        weekday_consumption_5to9 + weekday_consumption_9to17 + weekday_consumption_17to22 + weekday_consumption_22to5))
        weekday_consumption_9to17n = weekday_consumption_9to17 / ((
                        weekday_consumption_5to9 + weekday_consumption_9to17 + weekday_consumption_17to22 + weekday_consumption_22to5))
        weekday_consumption_17to22n = weekday_consumption_17to22 / ((
                        weekday_consumption_5to9 + weekday_consumption_9to17 + weekday_consumption_17to22 + weekday_consumption_22to5))
        weekday_consumption_22to5n = weekday_consumption_22to5 / ((
                        weekday_consumption_5to9 + weekday_consumption_9to17 + weekday_consumption_17to22 + weekday_consumption_22to5))

        # print(weekday_consumption_22to6n)

        # In case the user specifies the weekend consumption and allocated percentage

        if int(weekend_consumption_separate) == 1:
            weekend_consumption_5to9n = weekend_consumption_5to9 / ((
                    weekend_consumption_5to9 + weekend_consumption_9to17 + weekend_consumption_17to22 + weekend_consumption_22to5))
            weekend_consumption_9to17n = weekend_consumption_9to17 / ((
                    weekend_consumption_5to9 + weekend_consumption_9to17 + weekend_consumption_17to22 + weekend_consumption_22to5))
            weekend_consumption_17to22n = weekend_consumption_17to22 / ((
                    weekend_consumption_5to9 + weekend_consumption_9to17 + weekend_consumption_17to22 + weekend_consumption_22to5))
            weekend_consumption_22to5n = weekend_consumption_22to5 / ((
                    weekend_consumption_5to9 + weekend_consumption_9to17 + weekend_consumption_17to22 + weekend_consumption_22to5))

        # print(weekend_consumption_22to6n)

        #In the case the weekend_consumption_separate == 0
        if int(weekend_consumption_separate) == 0:
            avg_user_load_n[5:9] = round((weekday_consumption_5to9n * avg_monthly * 12 / (365 * 4)), 3)
            avg_user_load_n[9:17] = round((weekday_consumption_9to17n * avg_monthly * 12 / (365 * 8)), 3)
            avg_user_load_n[17:22] = round((weekday_consumption_17to22n * avg_monthly * 12 / (365 * 5)), 3)
            avg_user_load_n[22:24] = round((weekday_consumption_22to5n * avg_monthly * 12 * 0.29 / (365 * 2)), 3)
            avg_user_load_n[0:5] = round((weekday_consumption_22to5n * avg_monthly * 12 * 0.71 / (365 * 5)), 3)

        # Applying the daily consumption to the whole year
            avg_user_load_n = np.tile(avg_user_load_n, 365)

            # print(sum(user_load)/12)
        else:
            weekday_24 = np.array(([0] * 24), dtype=float)
            weekend_24 = np.array(([0] * 24), dtype=float)

            weekday_daily = round((avg_monthly * 12) / (261 + round(104 * (weekend_consumption_change + 1))))
            weekend_daily = round((weekend_consumption_change + 1) * weekday_daily)

            weekday_24[5:9] = round((weekday_consumption_5to9n * (weekday_daily) / 4), 3)
            weekday_24[9:17] = round((weekday_consumption_9to17n * (weekday_daily) / 8), 3)
            weekday_24[17:22] = round((weekday_consumption_17to22n * (weekday_daily) / 5), 3)
            weekday_24[22:24] = round((weekday_consumption_22to5n * (weekday_daily * 0.29) / 2), 3)
            weekday_24[0:5] = round((weekday_consumption_22to5n * (weekday_daily * 0.71) / 5), 3)

            weekend_24[5:9] = round((weekend_consumption_5to9n * (weekend_daily) / 4), 3)
            weekend_24[9:17] = round((weekend_consumption_9to17n * (weekend_daily) / 8), 3)
            weekend_24[17:22] = round((weekend_consumption_17to22n * (weekend_daily) / 5), 3)
            weekend_24[22:24] = round((weekend_consumption_22to5n * (weekend_daily * 0.29) / 2), 3)
            weekend_24[0:5] = round((weekend_consumption_22to5n * (weekend_daily * 0.71) / 5), 3)

            df_load = []

            for i in range(365):
                if days[i * 24] == 'Saturday' or days[i * 24] == 'Sunday':
                    df_load.extend(weekend_24)
                else:
                    df_load.extend(weekday_24)

            avg_user_load_n = df_load
            # print('Monthly',len(df_load))
        # date = date.today()
        # year = date.year
        # days_n =366 if calendar.isleap(year) else 365
        # end time
        end = time.time()

        runtime = (end - start)
        print('The runtime Monthly:', runtime)
        return TS, TOU, avg_user_load_n
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print('Error ', e);

def monthly_data():
    start = time.time()
    data = monthly()
    TS = data[0]
    TOU = data[1]
    avg_user_load_n = data[2]

    TS_TOU = {'date&time': TS, 'TOU': TOU}
    user_load = pd.DataFrame(TS_TOU)
    # avg_in_month_m = []
    # user_load['date&time'] = TS
    user_load['Load'] = avg_user_load_n
    # cumulated for every hour of the month
    user_load['cumulative'] = user_load.groupby((user_load['date&time']).dt.month)['Load'].cumsum()
    # user_load['TOU'] = TOU
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
    avg_in_month_m = user_load.resample('MS', on='date&time').Load.sum()
    avg_in_month_m_n = user_load.resample('MS', on='date&time').normal.sum()
    avg_in_month_m_p = user_load.resample('MS', on='date&time').peak.sum()
    avg_in_month_m_op = user_load.resample('MS', on='date&time').offpeak.sum()
    # print((user_load[0:24]))
    # print(avg_in_month_m, avg_in_month_m_n, avg_in_month_m_p, avg_in_month_m_op)
    # print(avg_in_month_m)
    # end time
    end = time.time()

    runtime = (end - start)
    print('The runtime Monthly2:', runtime)
    return avg_in_month_m, avg_in_month_m_n, avg_in_month_m_p, avg_in_month_m_op, user_load['Load']


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
# avg_in_month_m = [i * d_avg for i in days_in_month]

# print((monthly_data()[4][24:72]))


