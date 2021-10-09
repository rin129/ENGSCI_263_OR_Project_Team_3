from routeGeneration import *
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
from linearProgram import optimal_Routes

def alphaBetaFromAmB(a, m, b):
    # Taken from code by David L. Mueller
    #github dlmueller/PERT-Beta-Python
    first_numer_alpha = 2.0 * (b + 4 * m - 5 * a)
    first_numer_beta = 2.0 * (5 * b - 4 * m - a)
    first_denom = 3.0 * (b - a)
    second_numer = (m - a) * (b - m)
    second_denom = (b - a) ** 2
    second = (1 + 4 * (second_numer / second_denom))
    alpha = (first_numer_alpha / first_denom) * second
    beta = (first_numer_beta / first_denom) * second
    return alpha, beta

def generateTaskTime(a, m, b):
    
    alpha, beta = alphaBetaFromAmB(a, m, b)
    location = a
    scale = b - a
    
    taskTime = stats.beta.rvs(alpha, beta) * scale + location
    
    return taskTime

num_sims = 1000

weekDemands = np.genfromtxt("WoolworthsDemandsWeekdays.csv", dtype = int, delimiter = ',')

travel_durations = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 1, usecols = list(range(1,67)))    
travel_durations = np.delete(travel_durations, 55, 0)
travel_durations = np.delete(travel_durations, 55, 1)

simulation_costs = [0] * num_sims
simulation_overtime = [0] * num_sims
simulation_extra_trucks = [0] * num_sims

for sims in range(num_sims):

    cost = 0
    extra_trucks = 0
    overtime = 0

    for i in range(len(optimal_Routes)):

        sim_time = 0
        sim_demand = 0

        for j in range(len(optimal_Routes[i])):

            for k in range(len(stores)):
                if (optimal_Routes[i][j] == stores[k]):
                    store_index = k
                    break
            
            store_demand = np.random.choice(weekDemands[store_index], size = 1, replace = True)
            sim_demand += store_demand

            if (sim_time == 0):
                travel_time = distribution_time[store_index]
                sim_time += generateTaskTime(travel_time * 0.8, travel_time, travel_time * 1.4) + (7.5*60*store_demand)
            elif (j == len(optimal_Routes[i]) - 1):
                travel_time = duration_store[store_index] 
                sim_time += generateTaskTime(travel_time * 0.8, travel_time, travel_time * 1.4) + (7.5*60*store_demand)
                travel_time = distribution_time[store_index]
                sim_time += generateTaskTime(travel_time * 0.8, travel_time, travel_time * 1.4)
            else:
                travel_time = duration_store[store_index] 
                sim_time += generateTaskTime(travel_time * 0.8, travel_time, travel_time * 1.4) + (7.5*60*store_demand)

            duration_store = travel_durations[store_index]

        sim_time = sim_time/(60*60)
        sim_time = (math.ceil(sim_time*4))/4

        if (sim_demand > demand_threshold):
            extra_trucks += 1
            cost += (225 * 4)
        
        if (sim_time > 4):
            overtime += 1
            cost += 275 * (sim_time - 4) + 225 * 4

        else:
            cost += 225 * sim_time

    simulation_costs[sims] = cost
    simulation_extra_trucks[sims] = extra_trucks
    simulation_overtime[sims] = overtime

# Average cost based off simulation
print(np.mean(simulation_costs))

# 95% percentile interval of costs
simulation_costs.sort()
print(simulation_costs[25])
print(simulation_costs[975])

# percentgae of time extra trucks/routes are needed
print((np.sum(simulation_extra_trucks)/num_sims)*100)

# average number of trucks/routes needing overtime pay per schedule
print(np.sum(simulation_overtime)/num_sims)