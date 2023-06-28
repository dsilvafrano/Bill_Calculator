## To make a 3d plot of results
# surface plot for 2d objective function
#Packages required
import time
# starting time
import pandas as pd
import numpy as np
import plotly
import matplotlib
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

start = time.time()

from financial_calc import financial_calc
import optuna

from openpyxl import *

# Build an array of sample points
sl = 50


#Optuna
def objective(trial):
    x = trial.suggest_float("x", 1, 10,)
    y = trial.suggest_float("y", 0, 10,)
    x1 = [x,y]
    return (financial_calc(x1)[7])
#optuna optimiser
# sampler = {"x": [40.5, 45.5, 49.5], "y": [5.5, 10.5, 15.5]}
sampler = optuna.samplers.CmaEsSampler()
# sampler = optuna.samplers.GridSampler({'x': [20, 42.5, 45, 47.5, 50], 'y': [2.5, 5, 7.5, 15, 25]})
# sampler = optuna.samplers.GridSampler({'x': [40, 45, 49.5], 'y': [0.5, 7.5, 12.5]})
study = optuna.create_study(sampler=sampler)
study.optimize(objective,n_trials=50,catch=(TypeError,IndexError,))
# study.optimize(objective,catch=(TypeError,IndexError,))
# trials = study.get_trials()
# x_new = []
# y_new = []
# for trial in trials:
#     x_new.append(trial.params['x'])
#     y_new.append(trial.params['y'])
    # print(trial.params)
# study.best_params
print('Param:',study.best_params)
# print('Trial:',study.best_trial)
# print('All Trials', trials)
# print('Value:',study.best_value)


# Retrieve all trials as a pandas DataFrame
trials_df1 = study.trials_dataframe()
trials_df = trials_df1.sort_values('value')
print(trials_df1)
graph_x  = trials_df['params_x']
print(graph_x)
graph_y  = trials_df['params_y']
print(graph_y)
graph_r  = trials_df['value']
print(graph_r)
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

npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, amount_invested\
        ,  average_annualcashflow,s_unit_yr1,grid_contri,solar_contri,batt_contri,export_contri, Av_emission_CO2, \
        Yr1_units, Elec_bill_withoutDER,Elec_bill_withDER,shade_free_area = financial_calc(x1)
# Result = np.fromiter((financial_calc(x1)),dtype='float')
#printing the results
print('NPV = ' + str(npv))
print('payback year = ' + str(payback_year))
print('25 yr savings = ' + str(cum_cashflow))
print('return on investment = ' + str(roi))
print('% of savings in 25 yrs = ' + str((cum_cashflow / sum(Elec_bill_withoutDER)) * 100))
print('Grid contribution = ' + str(grid_contri))
print('Solar contribution = ' + str(solar_contri))
print('Batt contribution = ' + str(batt_contri))
print('Export contribution = ' + str(export_contri))
print('NPV(BAU) to dis.Savings = ' + str(100 - NPV_to_Savings))
print('Shade free area(m2) = ' + str(shade_free_area))
print('Avg. annual Savings = ' + str(average_annualcashflow))
print('Avg. solar gen for yr 1 = ' + str(s_unit_yr1))
print('Av_emission_CO2 for yr 1 = ' + str(Av_emission_CO2))
print('Load for yr 1 = ' + str(sum(Yr1_units)))
print('Electric bill w/o sys =' + str(sum(Elec_bill_withoutDER)))
print('Electric bill w sys =' + str(sum(Elec_bill_withDER)))
a1 = [x1[0], x1[1], npv, payback_year, cum_cashflow, roi, total_savings_bill, bau_npv, dis_saving, NPV_to_Savings, amount_invested\
        ,  average_annualcashflow,s_unit_yr1,grid_contri,solar_contri,batt_contri,export_contri, Av_emission_CO2, \
        Yr1_units, Elec_bill_withoutDER,Elec_bill_withDER,shade_free_area]
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

# fig1 = optuna.visualization.plot_slice(study)
# matplotlib.pyplot.show()

# # # create a surface plot with the jet color scheme
# figure = matplotlib.pyplot.figure()
# axis = matplotlib.pyplot.axes(projection='3d')
# # xaxis = [1, 2, 2, 2.9, 3.9, 4.43]
# # yaxis = [1,1,2,0.8,0.5,-0.33 ]
# # create a mesh from the axis
# # x, y = meshgrid(x_axis, y_axis)
# # z = meshgrid(x_axis, results)
# # results = [8.44, 0, 0, 29.48, 25.36, -3.5, 32.24, 20.97, 9.79]
# axis.plot_trisurf(graph_x, graph_y, graph_r, cmap='YlGn')
# # axis.get_axes_locator()
# #set axis and label for graph
# axis.set_title("3D plot", pad=25, size=15)
# axis.set_xlim(0, 50)
# axis.set_ylim(0, 50)
# axis.set_xlabel("Solar capacity (kW)")
# axis.set_ylabel("Battery capacity (kWh)")
# axis.set_zlabel("Parameter: NPV/NPV(bau)")
# show the plot

# Create a figure and add a 3D axis to it
fig = pyplot.figure(figsize=(10,5))
ax = fig.add_subplot(111, projection='3d')

# Extract the data for the x, y, and z axis
x = trials_df['params_x']
y = trials_df['params_y']
z = trials_df['value']

# Create a grid of points for the surface plot
# x_mesh, y_mesh = np.meshgrid(x, y)
# z_mesh = np.array([z])

# Plot the surface using the plot_surface method
ax.plot3D(x, y, z, "green")
ax.scatter3D(x, y, z, c='blue')

# Add labels to the x, y, and z axis
ax.set_xlabel('Solar capacity (kW)')
ax.set_ylabel('Battery capacity (kWh)')
ax.set_zlabel('Parameter: NPV/NPV(bau)')


# # Extract the data for the x, y, and z axis
# x = trials_df['params_x']
# y = trials_df['params_y']
# z = trials_df['value']
#
# # Create a grid of points for the heatmap plot
# x_unique = np.sort(np.unique(x))
# y_unique = np.sort(np.unique(y))
# x_mesh, y_mesh = np.meshgrid(x_unique, y_unique)
# z_mesh = np.reshape(z, (len(x_unique), len(y_unique)))
#
# # Plot the heatmap using the pcolormesh method
# pyplot.pcolormesh(x_mesh, y_mesh, z_mesh, cmap='viridis')
# pyplot.colorbar()
# pyplot.xlabel('params_x')
# pyplot.ylabel('params_y')
# pyplot.title('Heatmap of value')
# pyplot.show()

# Show the plot
# pyplot.savefig("images.png",dpi=250)

# Write an excel sheet
# writer = pd.ExcelWriter('Comparison.xlsx')
# wb = load_workbook('Comparison.xlsx')
# # with pd.ExcelWriter('Comparison.xlsx') as writer: trials_df.to_excel(writer, sheet_name='x2')
# ws = wb.create_sheet()
# ws.title = 'Sheet3'
# wb.active = wb['Sheet3']
# # ws = trials_dfq
# # ws = wb['Sheet2']
# trials_df.to_excel(writer, sheet_name='Sheet3')
# wb.save()
matplotlib.pyplot.show()