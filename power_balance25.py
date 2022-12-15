# Populate Load, Solar,Battery,Grid and Excess for 25 years
# Build a dataframe to store each field and escalate each field for 25 years
# Packages required
import time
# starting time
start = time.time()

import pandas as pd
import numpy as np
import Inputs
import SQL
from power_balance import power_balance
from SOC import SOC


# Inputs required
solar = Inputs.solar
battery = Inputs.battery
x1 = np.zeros(2, dtype=float)
x1[0] = Inputs.x1[0] # user input solar capacity
x1[1] = Inputs.x1[1] # user input storage capacity
bat_inv = 0.835 * x1[0]
socbatmax = Inputs.socmax * x1[1]
# print('SOC max', socbatmax)
socbatmin = SQL.socmin * x1[1]
# print('SOC min', socbatmin)
socin = Inputs.socin * x1[1]
load_esc = SQL.load_esc
der_deg = Inputs.der_deg
# print(der_deg)
batstatus = Inputs.batstatus
metering_type = Inputs.metering_type

def esc25():
    #Retrieve the information from power balance
    df_l = pd.DataFrame()
    df_s = pd.DataFrame()
    df_b = pd.DataFrame()
    df_g = pd.DataFrame()
    df_e = pd.DataFrame()
    df_rem = pd.DataFrame()
    df_exsol = pd.DataFrame()
    df_ch = pd.DataFrame()
    df_soc = pd.DataFrame()
    df_g_t = pd.DataFrame()

    df_batst = pd.DataFrame()

    df_a = power_balance(x1,0)
    df_l['year0'] = round(df_a[0]['load'],3)
    df_s['year0'] = round(df_a[0]['solar'],3)
    df_b['year0'] = round(df_a[0]['battery'],3)
    df_b['year0'] = np.where((df_b['year0'] < 0), 0, df_b['year0']).round(3)
    df_g['year0'] = round(df_a[0]['grid'],3)
    df_g_t['year0'] = df_g['year0']
    df_e['year0'] = round(df_a[0]['excess'],3)
    df_ch['year0'] = round(df_a[0]['ch&dch'], 3)
    df_soc['year0'] = round(df_a[0]['SOC'], 3)
    df_rem['year0'] = round(df_a[0]['rem load'], 3)
    df_exsol['year0'] = round(df_a[0]['exsolar'], 3)
    # df_exsol['year0'] = round(df_a[0]['exsolar'], 3)
    df_batst['year0'] = round(df_a[0]['batstatus'], 3)


    #Populating the dataframe
    for i in range (1,26):
        df_l['year' + str(i)] = df_a[0]['load'] * (1 + (i * load_esc))
        df_s['year' + str(i)] = df_a[0]['solar'] * (1 - (i * der_deg))
        df_batst['year' + str(i)] = df_batst['year0']
        df_rem['year' + str(i)] = (df_l['year' + str(i)]) - (df_s['year' + str(i)])
        df_rem['year' + str(i)][df_rem['year' + str(i)] < 0] = 0
        df_exsol['year' + str(i)] = (- df_l['year' + str(i)]) + (df_s['year' + str(i)])
        df_exsol['year' + str(i)][df_exsol['year' + str(i)] < 0] = 0

        if solar & battery:
            # define conditions for battery charge and discharge availibility
            cond_ch = [((df_batst['year' + str(i)] == -1) & (df_exsol['year' + str(i)] < bat_inv)),
                    ((df_batst['year' + str(i)] == -1) & (df_exsol['year' + str(i)] > bat_inv)),
                    ((df_batst['year' + str(i)] == 1) & (df_rem['year' + str(i)] < bat_inv)),
                    ((df_batst['year' + str(i)] == 1) & (df_rem['year' + str(i)] > bat_inv))]
            choice_ch = [df_exsol['year' + str(i)], bat_inv, df_rem['year' + str(i)], bat_inv]

            df_ch['year' + str(i)] = np.select(cond_ch,choice_ch)

            # Battery power for year i
            df_b['year' + str(i)] = SOC(df_ch['year' + str(i)]).round(3)
            # Removing all negative values to find sum of battery contribution
            df_b['year' + str(i)] = np.where((df_b['year' + str(i)] < 0), 0, df_b['year' + str(i)]).round(3)
            if metering_type == "Gross Metering":
                df_g['year' + str(i)] = round(df_l['year' + str(i)],3)
                df_e['year' + str(i)] = round(df_s['year' + str(i)] - df_b['year' + str(i)],3)
                #In case of Gross Metering with Battery, allocating battery for export
                df_e['year' + str(i)] = np.where((df_s['year' + str(i)] > 0),(df_s['year' + str(i)] - df_b['year' + str(i)]),
                                                 (df_b['year' + str(i)])).round(3)
            else:
                df_g_t['year' + str(i)] = round(df_l['year' + str(i)] - df_s['year' + str(i)] - df_b['year' + str(i)],
                                                3)  # allocating export and grid after battery
                df_g['year' + str(i)] = np.where((df_g_t['year' + str(i)] > 0), df_g_t['year' + str(i)], 0)
                df_e['year' + str(i)] = np.where((df_g_t['year' + str(i)] > 0), 0, (-df_g_t['year' + str(i)]))
                #      # what happens if battery has remaining energy? Does it go to excess DER?
        else:
            df_b['year' + str(i)] = np.zeros(8760)
            if metering_type == "Gross Metering":
                df_g['year' + str(i)] = round(df_l['year' + str(i)],3)
                df_e['year' + str(i)] = round(df_s['year' + str(i)],3)
            else:
                df_g['year' + str(i)] = round(df_rem['year' + str(i)],3)
                df_e['year' + str(i)] = round(df_exsol['year' + str(i)],3)

    # print(df_ch['year0'][0:24])
    # print(df_a[0][0:24])
    # print(df_b['year1'][0:24])
    # print(df_s['year1'][0:24])
    # print(df_g['year1'][0:24])
    # print(df_e['year1'][0:24])
    pb_df = pd.DataFrame()
    pb_df = [df_l, df_g, df_s, df_b, df_e]
    # print(pb_df[0:24])
    return pb_df

# print('The contents are:', sum(esc25()[0]['year1']))


# end time
end = time.time()

runtime = (end - start)
# print('The runtime power balance 25 year:', runtime)