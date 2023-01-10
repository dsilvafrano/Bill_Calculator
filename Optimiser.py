#Packages required
import time
# starting time
start = time.time()
import numpy as np
import pandas as pd
from financial_calc import financial_calc
from Inputs import solar, battery, sload
from scipy.optimize import minimize, basinhopping
#Define Input Method
inputmethod = 'optimize'
# Optimisation using Scipy

if inputmethod=='optimize':

# SLSQP optimization
    # define objective: maximize Return on investment
    def objective(x1, sign=-1):
        # print(type(x1))
        return sign * financial_calc(x1)[7]


# SHGO optimization
    # define eggholder: maximize saving percentage
    # def eggholder(x1, sign=-1):
    #     # print(type(x1))
    #     return sign * financial_calc(x1)[7]


    # def constraint2(x1):
    #     return 25 - financial_calc(x1)[1]
    #
    # def constraint3(x1):
    #     return financial_calc(x1)[7] - 10
    #
    #
    # con2 = {'type': 'ineq', 'fun': constraint2}
    # con3 = {'type': 'eq', 'fun': constraint3}
    #
    # cons = ([con3])

#Define bounds
    xx = np.zeros(2, dtype=float).round(3)
    # print(type(xx))
    if solar & battery:
        xx[0] = sload/4
        xx[1] = sload/8
        b = (1, sload)
        b1 = (0, sload * 2)
        bnds = (b, b1)
    else:
        xx[0] = sload/4
        xx[1] = 0
        b = (1, sload)
        b1 = (0, 0)
        bnds = (b, b1)

# show initial objective
    # SLSQP optimization
    print('Initial Objective: ' + str(-objective(xx)))


    # SHGO optimization
    # print('Initial Objective: ' + str(-eggholder(xx)))

    # Basin Hopping Optimisation
    # print('Initial Objective: ' + str(-objective(xx)))

    # Record value of objective
    # results_shgo = []
    # results_shgo.append(objective(xx))
    # x_list = []
    # x_list.append(xx[0])
    # y_list = []
    # y_list.append(xx[1])
 # For Call back
    def CB(xx):
        # print('In call back')

        x_value = round(xx[0],3)
        x_new = x_value
        y_value = round(xx[1],3)
        y_new = y_value
        r_value = -objective(xx)
        r_new = r_value
        group1 = (x_new, y_new, r_new)
        # df1 = pd.DataFrame()
        # df1['Solar'] = x_new
        # df1['Battery'] = y_new
        # df1['Func'] = r_new
        # print(df1)
        print(group1)

        return group1
        # return x_new, y_new, r_new,  # df1

# Optimisation function
    # SLSQP optimization
    solution = minimize(objective, xx, method='COBYLA', bounds=bnds, tol=1e-5, callback=CB, #constraints=cons,
                        options={'disp': True, 'maxiter': 5})

    # SHGO optimization
    # solution1 = shgo(eggholder, bounds=bnds, n=2, iters=1, callback=CB,sampling_method='simplicial')

    # Basin Hopping Optimisation
    # solution2 = basinhopping(objective, xx, niter=10, T=2.0, stepsize=10,
    #                          minimizer_kwargs={'method':'L-BFGS-B'}, take_step=None, accept_test=None,
    #                          callback=CB(xx), interval=20, disp=True, niter_success=None,
    #                          seed=None)

    # Goal seek optiimization
    # roi = 10
    # goal = roi
    #
    # solution = GoalSeek(objective,goal,xx)

# Saving Optimised result
    # SLSQP optimization
    x = solution.x

    # SHGO optimization
    # x = solution1.x
    # xmore = solution1.xl

    # Basin Hopping optimization
    # x = solution2.x

# show final objective
    # SLSQP optimization
    print(solution.x)

    # SHGO optimization
    # print(solution1.x)
    # print(solution1.x1)

    # Basin Hopping optimization
    # print(solution2.x)

# Display Final objective
    # SLSQP optimization
    # print('Final Objective: ' + str(-objective(x)))

    # SHGO optimization
    # print('Final Objective: ' + str(-eggholder(x)))

    # Basin Hopping optimization
    print('Final Objective: ' + str(-objective(x)))

# Printing Solution
    # print solution
    print('Solution')
    print('x1 = ' + str(x[0]))
    print('x2 = ' + str(x[1]))
    # print('x3 = ' + str(x[2]))


    npv1, pback_year, cum_cashflow, roi1, tot_savings, bau_npv, dis_saving, NPV_to_Savings, amount_invested = financial_calc(
        solution.x)

    # end time
    end = time.time()

    # total time taken
    print(f"Runtime of the program is {end - start}")
    runtime = (end - start)
    print('npv = ' + str(npv1))
    print('payback year = ' + str(pback_year))
    print('cumulative cash flow = ' + str(cum_cashflow))
    print('return on investment = ' + str(roi1))
    print('total savings on bill = ' + str(tot_savings))
    print('NPV for BAU = ' + str(bau_npv))
    print('Discounted Total Savings = ' + str(dis_saving))
    print('NPV(BAU) to dis.Savings = ' + str(NPV_to_Savings))
    a1 = [x[0], x[1], npv1, pback_year, cum_cashflow, roi1, tot_savings, runtime, amount_invested]
    print(a1)
    df = pd.DataFrame(a1)
    df = df.round(decimals=3)
    df.index = ['Solar capacity (kW)', 'Storage capacity (kWh)', 'npv of cashflow (INR)', 'payback year(years)',
                'cumulative cash flow(INR)', 'return on investment(%)', 'total savings on bill', 'runtime (sec)',
                'Installation cost (INR)']

    # df.to_excel('scipy_optresult_maxroi_scenario3.xlsx', header=None)

else:
# Customise run inputs and results display
    a =np.zeros(2, dtype=float).round(3)
    a[0] = 9.82 # user input solar capacity
    # # a[0]= 26.126338006179388 # user input solar capacity
    a[1]= 1.28 # user input storage capacity
    npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, amount_invested=financial_calc(a)

    end = time.time()
    # total time taken
    print(f"Runtime of the program is {end - start}")
    runtime = (end - start)


    print('NPV = ' + str(npv))
    print('payback year = ' + str(payback_year))
    print('cumulative cash flow = ' + str(cum_cashflow))
    print('return on investment = ' + str(roi))
    print('total savings on bill = ' + str(total_savings_bill))
    print('NPV for BAU = ' + str(bau_npv))
    print('Discounted Total Savings = ' + str(dis_saving))
    print('NPV(BAU) to dis.Savings = ' + str(NPV_to_Savings))
    a1 = [a[0], a[1], npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, amount_invested]
    print(a1)


# end time
end = time.time()

runtime = (end - start)
print('The runtime for Optimiser is:', runtime)