## To make a 3d plot of results
# surface plot for 2d objective function
#Packages required
import time
# starting time
import numpy as np

start = time.time()

from financial_calc import financial_calc
import optuna

# Build an array of sample points
sl = 25
# max_x: float = sl
# max_y: float = sl * 2
# min_x: float = 1
# min_y: float = 0
# r_x: float = sl * 0.05
# r_y: float = max_y * 0.05
# p_x: float = sl * 0.15
# p_y: float = max_y * 0.15
# q_x: float = sl * 0.25
# q_y: float = max_y * 0.25
# mid_x: float = max_x/2
# mid_y: float = max_y/2
# f_x: float = sl * 0.75
# f_y: float = max_y * 0.75
# g_x: float = sl * 0.85
# g_y: float = max_y * 0.85
# h_x: float = sl * 0.95
# h_y: float = max_y * 0.95
#
#
# list1 = [mid_x, f_x, max_x]
# list2 = [r_y, mid_y]
# sample = []
# for x in list1:
#     for y in list2:
#
#         arr = [x,y]
#         sample.append(arr)

# print('sample:',sample)

#Function
# def objective(x1):
#     return (financial_calc(x1)[7])

#Optuna
def objective(trial):
    x = trial.suggest_float("x", 1, 125)
    y = trial.suggest_float("y", 0, 125)
    x1 = [x,y]
    return (financial_calc(x1)[7])
#optuna optimiser
study = optuna.create_study()
study.optimize(objective, n_trials=5,catch=(TypeError,IndexError,))

# study.best_params
print('Param:',study.best_params)
print('Trial:',study.best_trial)
print('Value:',study.best_value)

#Run the finincial cal with best parameters
# Vfun = np.vectorize(financial_calc)
x = study.best_params.get('x')
# Vx = np.vectorize(x)
# print('The solar capacity is:',x)
y = study.best_params.get('y')
# Vy = np.vectorize(y)
# print('The battery capacity is:',y)
x1 = [x,y]
# x1 = [x,y]
# print('The array:', x1)
Result = financial_calc(x1)
# Result = np.fromiter((financial_calc(x1)),dtype='float')
#printing the results
print('NPV = ' + str(Result[0]))
print('payback year = ' + str(Result[1]))
print('cumulative cash flow = ' + str(Result[2]))
print('return on investment = ' + str(Result[3]))
print('total savings on bill = ' + str(Result[4]))
print('NPV for BAU = ' + str(Result[5]))
print('Discounted Total Savings = ' + str(Result[6]))
print('NPV(BAU) to dis.Savings = ' + str(100-Result[7]))
a1 = [x1[0], x1[1], Result]
print('The result is:', a1)

# obj = []
# # zaxis = []
# #Populating results
# for z in sample:
#         try:
#             obj.append([z, objective(z)])
#         except Exception:
#             obj.append([z, 0])
#             pass
#
# print('Result:', obj)
# x_axis = []
# y_axis = []
# results = []
#
# #Splitting the array
# for z in obj:
#     x_axis.append(z[0][0])
#     y_axis.append(z[0][1])
#     results.append(z[1])
#
# # end time
end = time.time()

runtime = (end - start)
print('The runtime for populating data is:', runtime)

# # create a surface plot with the jet color scheme
# figure = matplotlib.pyplot.figure()
# axis = matplotlib.pyplot.axes(projection='3d')
# # xaxis = [1, 2, 2, 2.9, 3.9, 4.43]
# # yaxis = [1,1,2,0.8,0.5,-0.33 ]
# # create a mesh from the axis
# # x, y = meshgrid(x_axis, y_axis)
# # z = meshgrid(x_axis, results)
# # results = [8.44, 0, 0, 29.48, 25.36, -3.5, 32.24, 20.97, 9.79]
# axis.plot_trisurf(x_axis, y_axis, results, cmap='YlGn')
# # axis.get_axes_locator()
# #set axis and label for graph
# axis.set_title("3D plot", pad=25, size=15)
# axis.set_xlim(mid_x, max_x)
# axis.set_ylim(r_y, mid_y)
# axis.set_xlabel("Solar capacity (kW)")
# axis.set_ylabel("Battery capacity (kWh)")
# axis.set_zlabel("Parameter: NPV/NPV(bau)")
# # show the plot
# matplotlib.pyplot.show()