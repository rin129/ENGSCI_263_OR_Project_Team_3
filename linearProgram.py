# ENGSCI 263 
# OR Project, Team 03

# This file conains the linear program which solves a Vehicle Routing Problem,
# so as to help advise Woolworths NZ in their finding of a least-cost routing schedule for their truck fleet. 

import numpy as np
import pandas as pd
from pulp import *
from routeGeneration import *

max_routes = 60

possible_routes = [i for i in range(0,650)]

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

print(routes[0])
print(routes[11])
print(routes[111])
print(routes[176])
print(routes[185])
print(routes[194])
print(routes[20])
print(routes[202])
print(routes[256])
print(routes[270])
print(routes[290])
print(routes[31])
print(routes[310])
print(routes[326])
print(routes[336])
print(routes[361])
print(routes[382])
print(routes[390])
print(routes[403])
print(routes[411])
print(routes[522])
print(routes[591])
print(routes[601])
print(routes[83])
