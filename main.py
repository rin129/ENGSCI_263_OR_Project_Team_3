# ENGSCI 263 
# OR Project, Team 03

# This is the main script file

from routeGeneration import *
from linearProgram import *
from simulationScript import *

from routeGenerationSat import *
from linearProgramSat import *
from simulationScriptSat import *

import matplotlib.pyplot as plt
import numpy as np

routes, hours, storesForLP = routeGeneration('WeekdayDemands.csv')
optimal_weekday_stores = linearProgram(routes, hours, storesForLP)
simulation_weekday_costs, simulation_weekday_extra_trucks, simulation_weekday_overtime = simulationScript(optimal_weekday_stores)

routes_sat, hours_sat, stores_sat, zero_demand_sat = routeGenerationSat('SaturdayDemand.csv')
optimal_sat_stores = linearProgramSat(routes_sat, hours_sat, stores_sat, zero_demand_sat)
simulation_sat_costs, simulation_sat_extra, simulation_sat_overtime = simulationScriptSat(optimal_sat_stores)

plt.hist(simulation_sat_costs, density=False, alpha=1, bins=20, edgecolor = 'black')
plt.title("1,000 simulations of weekend route schedule") 
plt.xlabel("Cost (NZD)")
plt.ylabel("Frequency")
plt.show()


'''
print(np.mean(simulation_weekday_costs))

# 95% percentile interval of costs
simulation_weekday_costs.sort()
print(simulation_weekday_costs[25])
print(simulation_weekday_costs[975])

# percentgae of time extra trucks/routes are needed
print((np.sum(simulation_weekday_extra_trucks)/1000)*100)

# average number of trucks/routes needing overtime pay per schedule
print(np.sum(simulation_weekday_overtime)/1000)

'''