# ENGSCI 263 
# OR project, Team 03

# This python script generates a list of feasible routes given average weekday deamnds 
# Using this python script routes are generated and the time taken for each route
# Routes are stored in a list with each index contating a route, each route being a list itself
# Time is stored in an array and each value is rounded up to the nearest quarter

import math
import numpy as np
from getUniqueItems import *

# store variable is just an array with each index being the name of each store
# 55th index deleted as this is the distribution centre and is not required

stores = np.genfromtxt('WoolworthsTravelDurations.csv', dtype = str, delimiter = ',', skip_footer = 66)
stores = stores[1:67]
stores = np.delete(stores, 55, 0)

# weekdayDeamnds variable is an array to store the average weekday demands of each store

### change the line below with the store you want to remove to compare results

weekdayDemands = np.genfromtxt('WeekdayDemands.csv', delimiter = ',', skip_header = 1, usecols = 2)

# travel_durations array is the 2d array for the time taken to travel between stores 
# distribution_time array is an array for the time taken to travel from the distribution centre to all the stores

travel_durations = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 1, usecols = list(range(1,67)))
distribution_time = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 56, skip_footer = 10, usecols = list(range(1,67)))
travel_durations = np.delete(travel_durations, 55, 0)
distribution_time = np.delete(distribution_time, 55, 0)
travel_durations = np.delete(travel_durations, 55, 1)

# create a time and demand threshold to set feasible routes
# the time threshold is in seconds and is 4 hours 
# demand threshold is 26 pallets

time_threshold = 240*60
demand_threshold = 26

# zero demand empty list stores the index positions of the stores with no demand on saturday

zero_demand = []
storesForLP = stores

# loop through all stores to find which ones have zero demand, store them in the zero_demand array

for a in range(len(weekdayDemands)):
    if (weekdayDemands[a] == 0):
        zero_demand.append(a)
        storesForLP = np.delete(storesForLP, a, 0)

# initialise the routes and hours array
# routes stores a list of all the routes
# hours stores the time taken for each route

routes = []
hours = []

# initialise time and demand constraints for each route

time = 0
demand = 0

# loop through all the stores

for i in range(len(stores)):

    travel_durations = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 1, usecols = list(range(1,67)))
    travel_durations = np.delete(travel_durations, 55, 0)
    travel_durations = np.delete(travel_durations, 55, 1)

    # smallest_visited array is an array that will contain the nearest 10 stores from the starting store already visited 

    smallest_visited = []
    smallest_visited.append(i)
    
    # next loop through the nearest 10 stores from the starting store

    for ii in range(10):

        no_demand = i in zero_demand

        if (no_demand == True):
            break

        # nodes_list variable contains the stores that the specific route has already visited to avoid repeats
        # next_visited is an array that contains the nearest 10 stores from one of the original 10 nearest store
        # next_store is the index position of one of the 10 nearest store

        nodes_list = []
        next_visited = []
        next_store = 0

        # visited boolean variable indicates if the store has been visited by the route so far
        # thisSmallest boolean varaible indicates if the store is one of the nearest 10 stores visited already
        # these booleans are to avoid repeats of routes 

        visited = False
        thisSmallest = False

        # duration store is a 1D array that contains the travel durations from the starting store to every other store 
        # append nodes_list (list that contains all the nodes) with the starting store

        no_demand = False

        duration_store = travel_durations[i]
        nodes_list.append(i)

        # first loop through all the stores to determine if any of the stores have routes generated based on the fact they are nearest 10 stores from the starting store
        # if the store is already part of the nearest 10 and has routes generated, set its travel duration to that store to be 0

        for l in range(len(duration_store)):
            thisSmallest = l in smallest_visited
            if (thisSmallest == True):
                duration_store[l] = 0

        # next loop through all stores to set the variable smallest
        # smallest is the shortest travel duration which is not zero

        for j in range(len(duration_store)):
            no_demand = j in zero_demand
            visited = j in nodes_list
            if ((duration_store[j] != 0) & (no_demand == False) & (visited == False)):
                smallest = duration_store[j]
                next_store = j
                break
        
        # loop to actually check which store has the shortest travel duration time
        # store the index position to next_store variable

        for k in range(len(duration_store)):
            thisSmallest = k in smallest_visited
            visited = k in nodes_list
            no_demand = k in zero_demand
            if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (thisSmallest == False) & (visited == False) & (no_demand == False)):
                smallest = duration_store[k]
                next_store = k

        # append the smallest_visited array with the variable next_store, one of the nearest 10 stores has been visited
        # append nodes_list to say the next_store has been visited

        smallest_visited.append(next_store)
        nodes_list.append(next_store)

        # from one of the nearest 10 stores, loop through the 10 stores nearest that store 

        for iii in range(10):

            # next_store_after is the variable that stores the index position of the nearest 10 stores from one of the 10 nearest stores of the original
            # time is the time taken for the route
            # demand is the demand used up for the route
            # route_list is an array of all the stores visited on that route
            # nodes_list is the index positions of the stores visited

            next_store_after = 0
            time = 0
            demand = 0
            route_list = []
            nodes_list = []

            # time so far is from distribution to starting store, time taken at that store, time taken to get to the next store and the time spent at the next store

            time = distribution_time[i] + (7.5*60*weekdayDemands[i]) + duration_store[next_store] + (7.5*60*weekdayDemands[next_store])

            # append route_list and nodes_list with the starting store and store after that

            route_list.append(stores[i])
            route_list.append(stores[next_store])
            nodes_list.append(i)
            nodes_list.append(next_store)

            # increase demand of store with demand at the first and second stores of the route
            # set duration_store to the travel times of the next store index

            demand += weekdayDemands[i] + weekdayDemands[next_store]
            duration_store = travel_durations[next_store]

            # visited, thisSmallest set initally to false
            # nextSmallest is the boolean to determine if this set of 10 nearest stores has been visited, or routes have been generated based off it already

            visited = False
            thisSmallest = False
            nextSmallest = False

            # first loop through all the stores to determine if any of the stores have routes generated based on the fact they are nearest 10 stores from the starting store
            # if the store is already part of the nearest 10 and has routes generated, set its travel duration to that store to be 0
            
            for l in range(len(duration_store)):
                no_demand = j in zero_demand
                nextSmallest = l in next_visited
                visited = l in nodes_list
                if ((nextSmallest == True) | (visited == True)):
                    duration_store[l] = 0

            # next loop through all stores to set the variable smallest
            # smallest is the shortest travel duration which is not zero

            for j in range(len(duration_store)):
                visited = j in nodes_list
                if ((duration_store[j] != 0) & (visited == False) & (no_demand == False)):
                    smallest = duration_store[j]
                    next_store_after = j
                    break

            # loop to actually check which store has the shortest travel duration time
            # store the index position to next_store variable

            for k in range(len(duration_store)):
                nextSmallest = k in next_visited
                visited = k in nodes_list
                no_demand = k in zero_demand
                if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (nextSmallest == False) & (visited == False) & (no_demand == False)):
                    smallest = duration_store[k]
                    next_store_after = k

            # append nodes_list with the next store after
            # append next_visited array
            # increase the demand count
            # increase the time count and include the time taken to travel from the next store after back to the distribution centre

            nodes_list.append(next_store_after)
            next_visited.append(next_store_after)
            demand += weekdayDemands[next_store_after]
            time += duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after]

            # conditional statement to check if the time and demand threshold has been met
            # if neither have been met then time is reduced and the route is finalised
            # if the condition is met the next store after can be added to the route and the time taken to get back to the distribution centre is subtracted
            # the back_home variable is a way to store the time taken to travel back home from the previous store
            # duration_store is the travel times from the next_store_after

            if ((time < time_threshold) & (demand <= demand_threshold)):
                back_home = distribution_time[next_store_after]
                time -= distribution_time[next_store_after]
                route_list.append(stores[next_store_after])
                duration_store = travel_durations[next_store_after]
                
            else: 
                time -= duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after]
                time += back_home
                back_home = 0

            # while loop to keep adding more stores to the route
            # the criteria to adding a store is if it is closest to the previous store and has not been visited before by the route    

            while ((time < time_threshold) & (demand <= demand_threshold)):

                # first for loop sets the smallest variable temporarily based on the fact that it has not been visited by the route already

                for j in range(len(duration_store)):
                    no_demand = j in zero_demand
                    visited = j in nodes_list
                    if ((duration_store[j] != 0) & (no_demand == False) & (visited == False)):
                        smallest = duration_store[j]
                        next_store_after = j
                        break
                
                # next for loop finds the actual smallest distance and stores the index position

                for k in range(len(duration_store)):
                    visited = k in nodes_list
                    no_demand = k in zero_demand
                    if ((duration_store[k] != 0) & (duration_store[k] < smallest) & (visited == False) & (no_demand == False)):
                        smallest = duration_store[k]
                        next_store_after = k

                # increase demand and time
                # append nodes_list with the next store

                demand += weekdayDemands[next_store_after]
                time += duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after]
                nodes_list.append(next_store_after)

                # check to see if the current route arrangement meets the threshold

                if ((time < time_threshold) & (demand <= demand_threshold)):
                    back_home = distribution_time[next_store_after]
                    time -= distribution_time[next_store_after]
                    route_list.append(stores[next_store_after])
                    duration_store = travel_durations[next_store_after]
                else: 
                    time -= duration_store[next_store_after] + (7.5*60*weekdayDemands[next_store_after]) + distribution_time[next_store_after]
                    time += back_home
                    back_home = 0

            # convert time from seconds to hours
            # multiply the time by 4, round it up to the nearest integer, then divide by 4 to get the answer as a quarter value
            # add the route to the list of routes
            # add the time to the list of hours

            route_list = getUniqueItems(route_list)

            time = time/(60*60)
            time = (math.ceil(time*4))/4
            routes.append(route_list)
            hours.append(time)

