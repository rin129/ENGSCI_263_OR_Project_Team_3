# ENGSCI 263 
# OR Project, Team 03

# This file contains the formulation and execution of a linear program which solves a Vehicle Routing Problem,
# so as to help advise Woolworths NZ in their finding of a least-cost routing schedule for their truck fleet. 

import numpy as np
import pandas as pd
from pulp import *

# The file "routeGeneration.py" generates multiple possible truck routes from the Distribution Centre to stores and back.
# The routes are generated with a time constraint, that is a maximum time on how long a truck may travel for along a route,
# as well as a demand constraint, that is the maximum number of pallets a truck can deliver along a route, due to capacity. 

# For our linear program, from "routeGeneration.py" we take in two lists: "routes", "hours" and "stores".
# "routes" is a list of a list, that contains all the possible routes generated, and the stores visited in those routes.
# "hours" is a list, that contains the travel time of each corresponding route generated from "routes".
# "stores" contains all the stores that need to be visited. 
from routeGeneration import routes, hours, storesForLP

# Number of trucks in the fleet, and number of shifts for operation. 
trucks = 30
shifts = 2

# The maximum number of routes that may be travelled, constrained by the shift and truck availability. 
max_routes = trucks * shifts 

# A list that stores the costs of all the possible routes. 
route_cost = []

# All the routes are costed @ $225 per hour for the first 4 hours travelled, and @ $275 for each hour traveled on top of the of that. 
# All routes times are to the nearest quarter of an hour, thus the routes are costed accordingly. 
for i in range(len(hours)):
    if hours[i] > 4:
        total_time = hours[i]
        extra_time = total_time - 4
        route_cost.append(extra_time * 275 + (total_time - extra_time) * 225)
    else:
        route_cost.append(hours[i] * 225) 

# Create a list for all the possible routes, using integers as the name for each route.
possible_routes = [i for i in range(0,len(routes))]

# Create a binary variable to state that a route is used. 
x = LpVariable.dicts("Route", possible_routes, 0, None, LpBinary)

# The varaible "prob" is created. 
prob = LpProblem("Woolworths NZ VRP", LpMinimize)

# The objective function, minimising the total costs of routes used in the schedule.  
prob += lpSum([route_cost[route] * x[route] for route in possible_routes])

# Availability constraint - total number of trucks and shifts available. 
prob += lpSum([x[route] for route in possible_routes]) <= max_routes

# Store constraint - each store can only be visited once. 
for store in storesForLP:
    prob += lpSum([x[route] for route in possible_routes if store in routes[route]]) == 1

# The problem data is written to an .lp file. 
prob.writeLP("WoolworthsVRP.lp")

# The problem is solved using PuLP's chocie of solver. 
prob.solve()

# The status of the problem is printed to the screen. 
print("Status:", LpStatus[prob.status])

optimal_Routes = []
optimal_Routes_times = []

# The name of the routes selected are printed to the screen. 
for route in prob.variables():
    if route.varValue == 1:
        index = (route.name).replace("Route_","")
        optimal_Routes.append(routes[int(index)])
        optimal_Routes_times.append(hours[int(index)])

hello = 0   