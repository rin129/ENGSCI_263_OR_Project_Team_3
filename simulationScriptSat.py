# ENGSCI 263 
# OR Project, Team 03

# This file simulates the optimal weekend schedule produced in the linearProgramSat.py file
# The average cost, average number of overtime shifts required for the schedule, and percetnage of time extra trucks are required for the schedule

from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import math

# two functions are required to model the varaince in traffic times
# the first function models the right-skew distribution
# the second function generates the times based on the distribution
# the first input a is the lower bound of the distribution, m is the expected value of the ditribution, b is the upper bound of the distribution

def alphaBetaFromAmB(a, m, b):
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

def simulationScriptSat(optimal_Routes):

    '''
    This function simulates the performance of the optimal routing schedule generating an array of costs, number of extra trucks, and number of overtime shfits

    Inputs: 

            optimal_Routes
            a list of a list of the routes in the optimal schedule

    Outputs:

            simulation_costs
            a list of the costs of running each simulation

            simulation_extra_trucks
            a list of the number of extra trucks needed for each simulation

            simulation_overtime
            a list of the number of overtime shifts needed for each simulation
    
    '''

    # setting demand threshold
    demand_threshold = 26

    # number of simulations required
    num_sims = 1000

    # list of all the stores

    stores = np.genfromtxt('WoolworthsTravelDurations.csv', dtype = str, delimiter = ',', skip_footer = 66)
    stores = stores[1:67]
    stores = np.delete(stores, 55, 0)

    stores = stores.tolist()

    distribution_time = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 56, skip_footer = 10, usecols = list(range(1,67)))
    distribution_time = np.delete(distribution_time, 55, 0)

    # weekend demands over the 4 week period, given that we are taking 4 weeks worth we only have 4 days worth of demands
    weekendDemands = np.genfromtxt("WoolworthsDemandsWeekend.csv", dtype = int, delimiter = ',', skip_header = 1, usecols = list(range(1,5)))

    # 2d array for travel_durations
    travel_durations = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 1, usecols = list(range(1,67)))    
    travel_durations = np.delete(travel_durations, 55, 0)
    travel_durations = np.delete(travel_durations, 55, 1)

    # arrays for simulation costs
    simulation_costs = [0] * num_sims
    simulation_overtime = [0] * num_sims
    simulation_extra_trucks = [0] * num_sims

    # loop through the number of simulations
    for sims in range(num_sims):

        # initlaise the cost, number of extra trucks, number of overtime shifts for the schedule

        cost = 0
        extra_trucks = 0
        overtime = 0

        # loop through the routes in the weekend schedule
        for i in range(len(optimal_Routes)):

            # initliase the time and demand for the route     
            sim_time = 0
            sim_demand = 0

            # loop through each store in the route
            for j in range(len(optimal_Routes[i])):
                
                # find the index position of the store currently in outer loop
                for k in range(len(stores)):
                    if (optimal_Routes[i][j] == stores[k]):
                        store_index = k
                        break
                
                # generate a random demand for pallets from the current store, this random allocation requires randomising with replacement
                # this is important because there are only 4 demand values from the data provided

                store_demand = np.random.choice(weekendDemands[store_index], size = 1, replace = True)
                sim_demand += store_demand

                # if the simulation time is still zero, generate an estimate of the time taken to get from the distribution store to the first store in the route using the right-skew distribution function
                # if the loop has reached the last store in the route, add the time taken to get between stores and from the last store to the distribution centre 
                # otherwise increment the time by taking an estimate of time between stores based on the right-skew distribution 

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

            # convert the route's time to hours and round up to the nearest quarter hour

            sim_time = sim_time/(60*60)
            sim_time = (math.ceil(sim_time*4))/4

            # if the demand for the route is greater than the threshold of 26, this means an extra truck is required
            # since the scheudle only uses 29 of a possible 60 trucks the cost for another truck can be assumed to be just the normal rate, $225 per hour
            # it is assumed that the extra truck on schedule will require 4 hours for their trip

            if (sim_demand > demand_threshold):
                extra_trucks += 1
                cost += (225 * 4)
            
            # if the total time taken to complete the route is greater than 4 hours, increment the overtime counter
            # increase the cost by accounting for the fact that overtime is 275 per hour, otherwise increase count based on the rate of $225 per hour

            if (sim_time > 4):
                overtime += 1
                cost += 275 * (sim_time - 4) + 225 * 4

            else:
                cost += 225 * sim_time

        # append the arrays for simulation results

        simulation_costs[sims] = cost
        simulation_extra_trucks[sims] = extra_trucks
        simulation_overtime[sims] = overtime

    return simulation_costs, simulation_extra_trucks, simulation_overtime

    '''

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

    plt.hist(simulation_costs, density=False, alpha=1, bins=20, edgecolor = 'black')
    plt.title("1,000 simulations of Saturday route schedule") 
    plt.xlabel("Cost (NZD)")
    plt.ylabel("Frequency")
    plt.show()

    '''