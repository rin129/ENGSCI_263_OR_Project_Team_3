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
import scipy.stats

# simulate weekday routes

routes, hours, storesForLP = routeGeneration('WeekdayDemands.csv')
optimal_weekday_stores = linearProgram(routes, hours, storesForLP)
simulation_weekday_costs, simulation_weekday_extra_trucks, simulation_weekday_overtime = simulationScript(optimal_weekday_stores)

# remove highland park and simulated weekday schedule costs

routes_HP, hours_HP, storesForLP_HP = routeGeneration('Removing_stores/Highland_Park-Aviemore_Drive/WeekdayDemands_Aviemore_Drive_Jumbo.csv')
optimal_weekday_stores_HP = linearProgram(routes_HP, hours_HP, storesForLP_HP)
simulation_weekday_costs_HP, simulation_weekday_extra_trucks_HP, simulation_weekday_overtime_HP = simulationScript(optimal_weekday_stores_HP)

# remove northwest and simulate weekday schedule costs

routes_NW, hours_NW, storesForLP_NW = routeGeneration('Removing_stores/Northwest-Westgate/WeekdayDemands_Westgate_Jumbo.csv')
optimal_weekday_stores_NW = linearProgram(routes_NW, hours_NW, storesForLP_NW)
simulation_weekday_costs_NW, simulation_weekday_extra_trucks_NW, simulation_weekday_overtime_NW = simulationScript(optimal_weekday_stores_NW)

# remove papakura and simulate weekday schedule costs

routes_PA, hours_PA, storesForLP_PA = routeGeneration('Removing_stores/Papakura-Roselands/WeekdayDemands_Roselands_Jumbo.csv')
optimal_weekday_stores_PA = linearProgram(routes_PA, hours_PA, storesForLP_PA)
simulation_weekday_costs_PA, simulation_weekday_extra_trucks_PA, simulation_weekday_overtime_PA = simulationScript(optimal_weekday_stores_PA)

fig1, ax1 = plt.subplots()
_, bins, _ = ax1.hist(simulation_weekday_costs, density=True, alpha=0, bins=20)
mean, sd = scipy.stats.norm.fit(simulation_weekday_costs)
weekday_bestFit = scipy.stats.norm.pdf(bins, mean, sd)
ax1.plot(bins, weekday_bestFit, 'k', label = 'Original Schedule')

_, bins_HP, _ = ax1.hist(simulation_weekday_costs_HP, density=True, alpha=0, bins=20)
mean_HP, sd_HP = scipy.stats.norm.fit(simulation_weekday_costs_HP)
weekday_bestFit_HP = scipy.stats.norm.pdf(bins_HP, mean_HP, sd_HP)
ax1.plot(bins_HP, weekday_bestFit_HP, 'b', label = "Highland Park removed")

_, bins_NW, _ = ax1.hist(simulation_weekday_costs_NW, density=True, alpha=0, bins=20)
mean_NW, sd_NW = scipy.stats.norm.fit(simulation_weekday_costs_NW)
weekday_bestFit_NW = scipy.stats.norm.pdf(bins_NW, mean_NW, sd_NW)
ax1.plot(bins_NW, weekday_bestFit_NW, 'r', label = "Northwest removed")

_, bins_PA, _ = ax1.hist(simulation_weekday_costs_PA, density=True, alpha=0, bins=20)
mean_PA, sd_PA = scipy.stats.norm.fit(simulation_weekday_costs_PA)
weekday_bestFit_PA = scipy.stats.norm.pdf(bins_PA, mean_PA, sd_PA)
ax1.plot(bins_PA, weekday_bestFit_PA, 'g', label = 'Papakura removed')

ax1.set(title = '1,000 simulations of weekday route schedule', xlabel = 'Cost (NZD)', ylabel = 'Probability Density')
ax1.legend()

# simulate saturday routes

routes_sat, hours_sat, stores_sat, zero_demand_sat = routeGenerationSat('SaturdayDemand.csv')
optimal_sat_stores = linearProgramSat(routes_sat, hours_sat, stores_sat, zero_demand_sat)
simulation_sat_costs, simulation_sat_extra, simulation_sat_overtime = simulationScriptSat(optimal_sat_stores)

routes_sat_HP, hours_sat_HP, stores_sat_HP, zero_demand_sat_HP = routeGenerationSat('SaturdayDemand.csv')
optimal_sat_stores_HP = linearProgramSat(routes_sat_HP, hours_sat_HP, stores_sat_HP, zero_demand_sat_HP)
simulation_sat_costs_HP, simulation_sat_extra_HP, simulation_sat_overtime_HP = simulationScriptSat(optimal_sat_stores_HP)

routes_sat_NW, hours_sat_NW, stores_sat_NW, zero_demand_sat_NW = routeGenerationSat('SaturdayDemand.csv')
optimal_sat_stores_NW = linearProgramSat(routes_sat_NW, hours_sat_NW, stores_sat_NW, zero_demand_sat_NW)
simulation_sat_costs_NW, simulation_sat_extra_NW, simulation_sat_overtime_NW = simulationScriptSat(optimal_sat_stores_NW)

routes_sat_PA, hours_sat_PA, stores_sat_PA, zero_demand_sat_PA = routeGenerationSat('SaturdayDemand.csv')
optimal_sat_stores_PA = linearProgramSat(routes_sat_PA, hours_sat_PA, stores_sat_PA, zero_demand_sat_PA)
simulation_sat_costs_PA, simulation_sat_extra_PA, simulation_sat_overtime_PA = simulationScriptSat(optimal_sat_stores_PA)

fig2, ax2 = plt.subplots()
_, bins_sat, _ = ax2.hist(simulation_sat_costs, density=True, alpha=0, bins=20)
mean_sat, sd_sat = scipy.stats.norm.fit(simulation_sat_costs)
sat_bestFit = scipy.stats.norm.pdf(bins, mean, sd)
ax2.plot(bins_sat, sat_bestFit, 'k', label = 'Original Schedule')

_, bins_sat_HP, _ = ax2.hist(simulation_sat_costs_HP, density=True, alpha=0, bins=20)
mean_sat_HP, sd_sat_HP = scipy.stats.norm.fit(simulation_sat_costs_HP)
sat_bestFit_HP = scipy.stats.norm.pdf(bins_sat_HP, mean_sat_HP, sd_sat_HP)
ax2.plot(bins_sat_HP, sat_bestFit_HP, 'b', label = "Highland Park removed")

_, bins_sat_NW, _ = ax2.hist(simulation_sat_costs_NW, density=True, alpha=0, bins=20)
mean_sat_NW, sd_sat_NW = scipy.stats.norm.fit(simulation_sat_costs_NW)
sat_bestFit_NW = scipy.stats.norm.pdf(bins_sat_NW, mean_sat_NW, sd_sat_NW)
ax2.plot(bins_sat_NW, sat_bestFit_NW, 'r', label = "Northwest removed")

_, bins_sat_PA, _ = ax2.hist(simulation_sat_costs_PA, density=True, alpha=0, bins=20)
mean_sat_PA, sd_sat_PA = scipy.stats.norm.fit(simulation_sat_costs_PA)
sat_bestFit_PA = scipy.stats.norm.pdf(bins_sat_PA, mean_sat_PA, sd_sat_PA)
ax2.plot(bins_sat_PA, sat_bestFit_PA, 'g', label = 'Papakura removed')

ax2.set(title = '1,000 simulations of saturday route schedule', xlabel = 'Cost (NZD)', ylabel = 'Probability Density')
ax2.legend()

plt.show()
