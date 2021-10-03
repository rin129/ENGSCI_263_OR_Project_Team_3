# ENGSCI 263 
# OR Project, Team 03

# This file conains the linear program which solves a Vehicle Routing Problem,
# so as to help advise Woolworths NZ in their finding of a least-cost routing schedule for their truck fleet. 

import numpy as np
import pandas as pd
from pulp import *
from routeGenerationSat import *

max_routes = 60

stores = np.delete(stores, zero_demand, 0)

possible_routes = [i for i in range(0,len(routes))]

x = LpVariable.dicts("Route", possible_routes, 0, None, LpBinary)

prob = LpProblem("Woolworths NZ VRP", LpMinimize)

prob += lpSum([225 * x[route] * hours[route] for route in possible_routes])

prob += lpSum([x[route] for route in possible_routes]) <= max_routes

for store in stores:
    prob += lpSum([x[route] for route in possible_routes if store in routes[route]]) == 1

prob.writeLP("WoolworthsVRP.lp")

prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
    if v.varValue == 1:
        print(v.name, "=", v.varValue)