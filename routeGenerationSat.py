# ENGSCI 263 
# OR project, Team 03

# This python script generates a list of feasible routes given average saturday deamnds 
# Using this python script routes are generated and the time taken for each route
# Routes are stored in a list with each index contating a route, each route being a list itself
# Time is stored in an array and each value is rounded up to the nearest quarter

# The following script works exactly the same way as routeGeneration except the demands are based on saturday average demands
# slight changes in code will be commented in this python script but to find general comments please view routeGeneration.py

import math
import numpy as np
from getUniqueItems import *

stores = np.genfromtxt('WoolworthsTravelDurations.csv', dtype = str, delimiter = ',', skip_footer = 66)
stores = stores[1:67]
stores = np.delete(stores, 55, 0)

# satDemands is an array for the average saturday demands

satDemands = np.genfromtxt('SaturdayDemand.csv', delimiter = ',', skip_header = 1, usecols = 2)

travel_durations = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 1, usecols = list(range(1,67)))
distribution_time = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 56, skip_footer = 10, usecols = list(range(1,67)))
travel_durations = np.delete(travel_durations, 55, 0)
distribution_time = np.delete(distribution_time, 55, 0)
travel_durations = np.delete(travel_durations, 55, 1)

time_threshold = 240*60
demand_threshold = 26

# zero demand empty list stores the index positions of the stores with no demand on saturday

zero_demand = []

# loop through all stores to find which ones have zero demand, store them in the zero_demand array

for a in range(len(satDemands)):
    if (satDemands[a] == 0):
        zero_demand.append(a)

routes = []
hours = []

time = 0
demand = 0

for i in range(len(stores)):

    smallest_visited = []
    smallest_visited.append(i)
    
    for ii in range(10):

        # this checks if the starting store has no demand
        # if the store has no demand then break out of the route generation loop for that store as no routes can be generated
        # the no_demand boolean variable prevents routes being generated that include stores with zero demand

        no_demand = i in zero_demand

        if (no_demand == True):
            break

        nodes_list = []
        next_visited = []
        next_store = 0

        visited = False
        thisSmallest = False
        no_demand = False

        duration_store = travel_durations[i]
        nodes_list.append(i)

        for l in range(len(duration_store)):
            thisSmallest = l in smallest_visited
            if (thisSmallest == True):
                duration_store[l] = 0

        # this for loop sets the smallest variable
        # it will set smallest to a store with zero demand

        for j in range(len(duration_store)):
            no_demand = j in zero_demand
            visited = j in nodes_list
            if ((duration_store[j] != 0) & (no_demand == False) & (visited == False)):
                smallest = duration_store[j]
                next_store = j
                break
        
        # this for loop includes the no_demand boolean variable

        for k in range(len(duration_store)):
            thisSmallest = k in smallest_visited
            visited = k in nodes_list
            no_demand = k in zero_demand
            if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (thisSmallest == False) & (visited == False) & (no_demand == False)):
                smallest = duration_store[k]
                next_store = k

        smallest_visited.append(next_store)
        nodes_list.append(next_store)

        for iii in range(10):

            next_store_after = 0
            time = 0
            demand = 0
            route_list = []
            nodes_list = []

            time = distribution_time[i] + (7.5*60*satDemands[i]) + duration_store[next_store] + (7.5*60*satDemands[next_store])
            route_list.append(stores[i])
            route_list.append(stores[next_store])
            nodes_list.append(i)
            nodes_list.append(next_store)
            demand += satDemands[i] + satDemands[next_store]
            duration_store = travel_durations[next_store]

            visited = False
            thisSmallest = False
            nextSmallest = False

            for l in range(len(duration_store)):
                nextSmallest = l in next_visited
                visited = l in nodes_list
                if ((nextSmallest == True) | (visited == True)):
                    duration_store[l] = 0

            for j in range(len(duration_store)):
                no_demand = j in zero_demand
                visited = j in nodes_list
                if ((duration_store[j] != 0) & (no_demand == False) & (visited == False)):
                    smallest = duration_store[j]
                    next_store_after = j
                    break

            for k in range(len(duration_store)):
                nextSmallest = k in next_visited
                visited = k in nodes_list
                no_demand = k in zero_demand
                if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (nextSmallest == False) & (visited == False) & (no_demand == False)):
                    smallest = duration_store[k]
                    next_store_after = k

            nodes_list.append(next_store_after)
            next_visited.append(next_store_after)
            demand += satDemands[next_store_after]
            time += duration_store[next_store_after] + (7.5*60*satDemands[next_store_after]) + distribution_time[next_store_after]

            if ((time < time_threshold) & (demand <= demand_threshold)):
                back_home = distribution_time[next_store_after]
                time -= distribution_time[next_store_after]
                route_list.append(stores[next_store_after])
                duration_store = travel_durations[next_store_after]
                
            else: 
                time -= duration_store[next_store_after] + (7.5*60*satDemands[next_store_after]) + distribution_time[next_store_after] - back_home
                time += back_home
                back_home = 0

            while ((time < time_threshold) & (demand <= demand_threshold)):

                for j in range(len(duration_store)):
                    no_demand = j in zero_demand
                    visited = j in nodes_list
                    if ((duration_store[j] != 0) & (no_demand == False) & (visited == False)):
                        smallest = duration_store[j]
                        next_store_after = j
                        break

                for k in range(len(duration_store)):
                    visited = k in nodes_list
                    no_demand = k in zero_demand
                    if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (visited == False) & (no_demand == False)):
                        smallest = duration_store[k]
                        next_store_after = k

                demand += satDemands[next_store_after]
                time += duration_store[next_store_after] + (7.5*60*satDemands[next_store_after]) + distribution_time[next_store_after]
                nodes_list.append(next_store_after)

                if ((time < time_threshold) & (demand <= demand_threshold)):
                    back_home = distribution_time[next_store_after]
                    time -= distribution_time[next_store_after]
                    route_list.append(stores[next_store_after])
                    duration_store = travel_durations[next_store_after]
                else: 
                    time -= duration_store[next_store_after] + (7.5*60*satDemands[next_store_after]) + distribution_time[next_store_after]
                    time += back_home
                    back_home = 0

            route_list = getUniqueItems(route_list)

            time = time/(60*60)
            time = (math.ceil(time*4))/4
            routes.append(route_list)
            hours.append(time)
