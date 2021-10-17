# ENGSCI 263 
# OR Project, Team 03

# This is the main script file

from routeGeneration import *
from linearProgram import *
from simulationScript import *

import matplotlib.pyplot as plt
import numpy as np

routes, hours, storesForLP = routeGeneration('WeekdayDemands.csv')
optimal_weekday_stores = linearProgram(routes, hours, storesForLP)
simulation_weekday_costs, simulation_weekday_extra_trucks, simulation_weekday_overtime = simulationScript('WoolworthsDemandsWeekdays.csv', optimal_weekday_stores)

print(np.mean(simulation_weekday_costs))

# 95% percentile interval of costs
simulation_weekday_costs.sort()
print(simulation_weekday_costs[25])
print(simulation_weekday_costs[975])

# percentgae of time extra trucks/routes are needed
print((np.sum(simulation_weekday_extra_trucks)/1000)*100)

# average number of trucks/routes needing overtime pay per schedule
print(np.sum(simulation_weekday_overtime)/1000)

plt.hist(simulation_weekday_costs, density=False, alpha=1, bins=20, edgecolor = 'black')
plt.title("1,000 simulations of weekday route schedule") 
plt.xlabel("Cost (NZD)")
plt.ylabel("Frequency")
plt.show()