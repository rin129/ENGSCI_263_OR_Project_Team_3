# returns a list of a list, or a data frame of the 60 different trips for a schedule.

# route generation by an algortihm

# create a list of nodes/stores at a region

import numpy as np

stores = np.genfromtxt('WoolworthsTravelDurations.csv', dtype = str, delimiter = ',', skip_footer = 66)
stores = stores[1:67]
stores = np.delete(stores, 55, 0)

travel_durations = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 1, usecols = list(range(1,67)))
distribution_time = np.genfromtxt('WoolworthsTravelDurations.csv', delimiter = ',', skip_header = 56, skip_footer = 10, usecols = list(range(1,67)))
travel_durations = np.delete(travel_durations, 55, 0)

time_threshold = 240*60
demand_threshold = 26

routes = []

time = 0
demand = 0

for i in range(len(stores)):
    time = 0
    demand = 0
    route_list = []
    duration_store = travel_durations[i]
    time = distribution_time[i] + (7.5*60)
    route_list.append(stores[i])
    # demand += demands[i]
    while ((time < time_threshold) & (demand < demand_threshold)):
        for j in range(len(duration_store)):
            if (duration_store[j] != 0):
                smallest = duration_store[j]
                break

        for k in range(len(duration_store)):
            if (duration_store[k] < smallest):
                smallest = duration_store[k]
                next_store = k
        # demand += demands[i]
        time += stores[next_store] + (7.5*60) + distribution_time[next_store]
        if (time < time_threshold & demand < demand_threshold):
            time -= distribution_time[next_store]
            distribution_time[next_store] = 0
            route_list.append(stores[next_store])

    routes.append(route_list)

print(routes)

