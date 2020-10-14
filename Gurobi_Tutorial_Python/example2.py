#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 12:51:32 2019

@author: tomas
"""

from gurobipy import * #Calls Gurobi Package
import numpy as np #Calls numpy Package
import pandas as pd

m= Model('Example 2')

#a Cont. Variable thats is greater than zero
x = m.addVar(vtype=GRB.CONTINUOUS,lb=0, name ='x')
#a Cont. Variable thats is greater than 2 and less than 5
x = m.addVar(vtype=GRB.CONTINUOUS,lb=2,ub=5, name ='x')
#an Integer. Variable thats is greater than 2 and less than 5
x = m.addVar(vtype=GRB.INTEGER,lb=2,ub=5, name ='x')
x = m.addVar(vtype=GRB.BINARY, name ='x') #a Binary. Variable
x = m.addVar(vtype=GRB.BINARY, name ='x') #a Binary. Variable
# defines a list of 10 varriables
z=y=x = [m.addVar(vtype=GRB.BINARY, name ='x%d' % J) for J in range(10)]
# defines a Series of 10 varriables
x = pd.Series([m.addVar(vtype=GRB.BINARY, name ='x%d' % J) for J in range(10)],
                                index=  [i for i in range(10)])

#Adding $\color{ForestGreen}x_{ijk}$ using Dataframes"
Index = [(i,j,k) for i in range (5) for j in range(5) for k in range(7)]
var = [m.addVar(lb=0, vtype=GRB.CONTINUOUS, name = "X"+str(i)) for i in Index]
demand = [np.random.randint(300,700) for i in Index]
x = pd.DataFrame({'x':var, 'demand':demand},
index = pd.MultiIndex.from_tuples(Index, names=['i', 'j','k']))

#Different ways to add constraints
m.addConstr(x+y>0)
m.addConstrs((x[i]>=0 for i in range(5)), name='Constraint')
m.addConstrs(z[i] == max_(x[i], y[i]) for i in range(5))
#Constraints can also be added using pandas' functions
