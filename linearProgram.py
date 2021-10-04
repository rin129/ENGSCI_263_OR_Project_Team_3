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
from routeGeneration import routes, hours, stores

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
for store in stores:
    prob += lpSum([x[route] for route in possible_routes if store in routes[route]]) == 1

# The problem data is written to an .lp file. 
prob.writeLP("WoolworthsVRP.lp")

# The problem is solved using PuLP's chocie of solver. 
prob.solve()

# The status of the problem is printed to the screen. 
print("Status:", LpStatus[prob.status])

# The name of the routes selected are printed to the screen. 
for route in prob.variables():
    if route.varValue == 1:
        print(route)

print(routes[100])
print(routes[1041])
print(routes[1542])
print(routes[1681])
print(routes[1893])
print(routes[1941])
print(routes[205])
print(routes[2133])
print(routes[2277])
print(routes[2381])
print(routes[2496])
print(routes[2591])
print(routes[2963])
print(routes[3026])
print(routes[3117])
print(routes[3229])
print(routes[3435])
print(routes[3539])
print(routes[3605])
print(routes[3971])
print(routes[4158])
print(routes[4244])
print(routes[482])
print(routes[5021])
print(routes[5186])
print(routes[5637])
print(routes[5771])
print(routes[6104])
print(routes[741])
print(routes[81])
print(routes[828])
print(routes[935])
