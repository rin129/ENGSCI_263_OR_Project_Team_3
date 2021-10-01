# returns a list of a list, or a data frame of the 60 different trips for a schedule.

# route generation by an algortihm

# create a list of nodes/stores at a region

import math
import numpy as np

stores = np.genfromtxt('WoolworthsTravelDurations.csv', dtype = str, delimiter = ',', skip_footer = 66)
stores = stores[1:67]
stores = np.delete(stores, 55, 0)

weekdayDemands = np.genfromtxt('WeekdayDemands.csv', delimiter = ',', skip_header = 1, usecols = 2)

travel_durations = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 1, usecols = list(range(1,67)))
distribution_time = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 56, skip_footer = 10, usecols = list(range(1,67)))
travel_durations = np.delete(travel_durations, 55, 0)
distribution_time = np.delete(distribution_time, 55, 0)
travel_durations = np.delete(travel_durations, 55, 1)

time_threshold = 240*60
demand_threshold = 26

routes = []
hours = []

time = 0
demand = 0

for i in range(len(stores)):
    smallest_visited = []
    smallest_visited.append(i)
    for ii in range(20):
        next_store = 0
        time = 0
        demand = 0
        route_list = []
        nodes_list = []

        duration_store = travel_durations[i]
        time = distribution_time[i] + (7.5*60*weekdayDemands[i]) 
        route_list.append(stores[i])
        nodes_list.append(i)
        demand += weekdayDemands[i]

        visited = False
        thisSmallest = False

        for l in range(len(duration_store)):
            thisSmallest = l in smallest_visited
            if (thisSmallest == True):
                duration_store[l] = 0

        for j in range(len(duration_store)):
            if (duration_store[j] != 0):
                smallest = duration_store[j]
                next_store = j
                break

        for k in range(len(duration_store)):
            thisSmallest = k in smallest_visited
            visited = k in nodes_list
            if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (thisSmallest == False) & (visited == False)):
                smallest = duration_store[k]
                next_store = k

        nodes_list.append(next_store)
        smallest_visited.append(next_store)
        demand += weekdayDemands[next_store]
        time += duration_store[next_store] + (7.5*60*weekdayDemands[next_store]) + distribution_time[next_store]

        if ((time < time_threshold) & (demand <= demand_threshold)):
            time -= distribution_time[next_store]
            route_list.append(stores[next_store])
            duration_store = travel_durations[next_store]
            
        else: 
            time -= duration_store[next_store] + (7.5*60*weekdayDemands[next_store]) + distribution_time[next_store] - back_home

        while ((time < time_threshold) & (demand <= demand_threshold)):

            for j in range(len(duration_store)):
                if (duration_store[j] != 0):
                    smallest = duration_store[j]
                    next_store = j
                    break

            for k in range(len(duration_store)):
                visited = k in nodes_list
                if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (visited == False)):
                    smallest = duration_store[k]
                    next_store = k

            demand += weekdayDemands[next_store]
            time += duration_store[next_store] + (7.5*60*weekdayDemands[next_store]) + distribution_time[next_store]
            nodes_list.append(next_store)

            if ((time < time_threshold) & (demand <= demand_threshold)):
                back_home = distribution_time[next_store]
                time -= distribution_time[next_store]
                route_list.append(stores[next_store])
                duration_store = travel_durations[next_store]
            else: 
                time -= duration_store[next_store] + (7.5*60*weekdayDemands[next_store]) + distribution_time[next_store]
                time += back_home
                back_home = 0

        time = time/(60*60)
        time = (math.ceil(time*4))/4
        routes.append(route_list)
        hours.append(time)

time = 0

