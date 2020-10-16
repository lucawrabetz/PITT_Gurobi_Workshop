import sys
import math
import random
import itertools
from gurobipy import *

n=100#NUMBER OF CITIES

# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where):
    # when does the callback act? 

        # make a list of edges selected in the solution

        # find the shortest cycle in the selected edge list

        # check that subtour != all nodes
        
            # add subtour elimination constraint for every pair of cities in tour
            


# Given a tuplelist of edges, find the shortest subtour

def subtour(edges):
    unvisited = list(range(n))
    cycle = range(n+1) # initial length has 1 more city
    while unvisited: # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

# Create n random points

random.seed(1) #fixes the seed, this guarantees the same output on each run
points = [(random.randint(0,100),random.randint(0,100)) for i in range(n)]


# Dictionary of Euclidean distance between each pair of points
dist = {(i,j) :
    math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
    for i in range(n) for j in range(i)}

# Create Model

# Create variables - remember the opposite edge!





# Add degree-2 constraint


# Optimize model



vals = m.getAttr('x', vars)
selected = tuplelist((i,j) for i,j in vals.keys() if vals[i,j] > 0.5)

tour = subtour(selected)
assert len(tour) == n

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.objVal)
print('')
