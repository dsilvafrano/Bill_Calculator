# Build TOU matrix for cost selection
import calendar
import time

# starting time
#Packages required
import Inputs
import pandas as pd
import SQL
import os
import sys


def tou():
    start = time.time()
    try:
        tariff_id = Inputs.tariff_id
        voltage_id = Inputs.voltage_id
        state_id = Inputs.state_id
        conn = SQL.create_connection()
        # tou_select_q = pd.read_sql_query(
        #     "select applicability_periods from tou_applicability_periods where state_id=" + str(
        #         state_id) + " and tariff_type_id=" + str(tariff_id) + " and voltage_type_id=" + str(voltage_id), conn)
        # tou_select = int(tou_select_q.values[0])
        tou_select = SQL.tou_select

        # Matrix for applying TOU
        if tou_select == 0:
        # Build matrix with 8760 points for normal period (i.e. = 1)
            tou_matrix = [1] * 8760
            # print(len(tou_matrix))
        elif tou_select == 1 or tou_select == 2:# 1 means applicable and 2 means optional
            tou_matrix = [1] * 24
            # print(tou_matrix)
        #identify max rows applicable for the inputs
            tou_period_q = pd.read_sql_query("select tou_period from tou_period_table where tariff_id=" + str(tariff_id) + " and voltage_id=" + str(voltage_id) + " and state_id=" + str(state_id), conn)
            tou_period = tou_period_q
            # print('check:', tou_period)
            tou_from_q = pd.read_sql_query("select tou_from_hr from tou_period_table where tariff_id=" + str(tariff_id) + " and voltage_id=" + str(voltage_id) + " and state_id=" + str(state_id), conn)
            tou_from:float = tou_from_q
            # print('check from:', tou_from)
            tou_to_q = pd.read_sql_query("select tou_to_hr from tou_period_table where tariff_id=" + str(tariff_id) + " and voltage_id=" + str(voltage_id) + " and state_id=" + str(state_id), conn)
            tou_to:float = tou_to_q
            # print('check from:', tou_to)
            tou_from_to = []
            tou_from_to = tou_period
            # print('The length of TOU is:', len(tou_period))
            df = pd.DataFrame(tou_from_to)
            df['tou_from_hr'] = tou_from
            df['tou_to_hr'] = tou_to
            # print('Period:', df)
            # print(tou_matrix[0:10])
            # print(df['tou_from_hr'][0])
            # print(len(tou_period))
        # Replacing the tou matrix with applicable peak (2) and off peak (3) periods
            # initialising range in tou matrix
            for u in range(len(tou_period)):
                if df['tou_period'][u] == 2:
                    r1, r2 = df['tou_from_hr'][u], df['tou_to_hr'][u]
                    r = 2
                elif df['tou_period'][u] == 3:
                    r1, r2 = df['tou_from_hr'][u], df['tou_to_hr'][u]
                    r = 3
                tou_matrix[r1:r2] = [r] * (r2 - r1)
            # print('TOU Matrix:',tou_matrix)

            tou_matrix = tou_matrix * 365
            # print((tou_matrix))

        # end time
        # end = time.time()
        #
        # runtime = (end - start)
        # print('The runtime TOU:', runtime)
        # end time
        end = time.time()

        runtime = (end - start)
        print('The runtime TOU matrix:', runtime)
        return tou_matrix, tou_select
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print('Error ', e);