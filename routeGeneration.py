# ENGSCI 263 
# OR project, Team 03

# This python script generates a list of feasible routes given average weekday deamnds 
# Using this python script routes are generated and the time taken for each route
# Routes are stored in a list with each index contating a route, each route being a list itself
# Time is stored in an array and each value is rounded up to the nearest quarter

import math
import numpy as np

# store variable is just an array with each index being the name of each store
# 55th index deleted as this is the distribution centre and is not required

stores = np.genfromtxt('WoolworthsTravelDurations.csv', dtype = str, delimiter = ',', skip_footer = 66)
stores = stores[1:67]
stores = np.delete(stores, 55, 0)

# weekdayDeamnds variable is an array to store the average weekday demands of each store

weekdayDemands = np.genfromtxt('WeekdayDemands.csv', delimiter = ',', skip_header = 1, usecols = 2)

# travel_durations array is the 2d array for the time taken to travel between stores 
# distribution_time array is an array for the time taken to travel from the distribution centre to all the stores

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
    
    for ii in range(10):

        nodes_list = []
        next_visited = []
        next_store = 0

        visited = False
        thisSmallest = False

        duration_store = travel_durations[i]
        nodes_list.append(i)

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

        smallest_visited.append(next_store)
        nodes_list.append(next_store)

        for iii in range(10):

            next_store_after = 0
            time = 0
            demand = 0
            route_list = []
            nodes_list = []

            time = distribution_time[i] + (7.5*60*weekdayDemands[i]) + duration_store[next_store] + (7.5*60*weekdayDemands[next_store])
            route_list.append(stores[i])
            route_list.append(stores[next_store])
            nodes_list.append(i)
            nodes_list.append(next_store)
            demand += weekdayDemands[i] + weekdayDemands[next_store]
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
                if (duration_store[j] != 0):
                    smallest = duration_store[j]
                    next_store_after = j
                    break

            for k in range(len(duration_store)):
                nextSmallest = k in next_visited
                visited = k in nodes_list
                if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (nextSmallest == False) & (visited == False)):
                    smallest = duration_store[k]
                    next_store_after = k

            nodes_list.append(next_store_after)
            next_visited.append(next_store_after)
            demand += weekdayDemands[next_store_after]
            time += duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after]

            if ((time < time_threshold) & (demand <= demand_threshold)):
                back_home = distribution_time[next_store_after]
                time -= distribution_time[next_store_after]
                route_list.append(stores[next_store_after])
                duration_store = travel_durations[next_store_after]
                
            else: 
                time -= duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after] - back_home
                time += back_home
                back_home = 0

            while ((time < time_threshold) & (demand <= demand_threshold)):

                for j in range(len(duration_store)):
                    if (duration_store[j] != 0):
                        smallest = duration_store[j]
                        next_store_after = j
                        break

                for k in range(len(duration_store)):
                    visited = k in nodes_list
                    if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (visited == False)):
                        smallest = duration_store[k]
                        next_store_after = k

                demand += weekdayDemands[next_store_after]
                time += duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after]
                nodes_list.append(next_store_after)

                if ((time < time_threshold) & (demand <= demand_threshold)):
                    back_home = distribution_time[next_store_after]
                    time -= distribution_time[next_store_after]
                    route_list.append(stores[next_store_after])
                    duration_store = travel_durations[next_store_after]
                else: 
                    time -= duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after]
                    time += back_home
                    back_home = 0

            time = time/(60*60)
            time = (math.ceil(time*4))/4
            routes.append(route_list)
            hours.append(time)

time = 0

