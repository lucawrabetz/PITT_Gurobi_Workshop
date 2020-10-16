# -*- coding: utf-8 -*-
"""
Modified on Tue Oct 29 21:34:30 2019
@author: tol28
Created on Mon Nov 13 20:13:09 2017
@author: hamdy
"""


from gurobipy import * #Calls Gurobi Package


#Is better to create models within functions:
    #This allows the momory of the model to be
    #released once the function returns

def solve_example_1(a1x,a1y,a2x,a2y,b1,b2,cx,cy,debug=0):
    #Model Definition
    m= Model('Example 1')

    #Varriables
    x = m.addVar(vtype=GRB.CONTINUOUS,lb=0, name ='x')
    y = m.addVar(vtype=GRB.CONTINUOUS,lb=0, name ='y')
    m.update()

    #Constraints
#    m.addConstr(5*x+2*y <= 10)
#    m.addConstr(3*x+5*y <= 12)
    con1=m.addConstr(a1x*x+a1y*y <= b1,name='c1')
    con2=m.addConstr(a2x*x+a2y*y <= b2,name='c2')

    #Objective Function
#    m.setObjective(3*x + 4*y, GRB.MAXIMIZE)
    m.setObjective(cx*x + cy*y, GRB.MAXIMIZE)
    m.optimize()
    
    if m.status == GRB.Status.OPTIMAL:
        if debug: print('Optimal objective: %g' % m.objVal)
        #You can also get the reference of variables or 
        # constraints by the name you gave them at its creation
        return (m.objVal, m.getVarByName("x").x, y.x,
                con1.pi, m.getConstrByName("c2").pi);
    elif m.status == GRB.Status.INFEASIBLE:
        if debug: print('Model is infeasible')
        m.computeIIS()
        if debug: print('\nThe following constraint(s) cannot be satisfied:')
        for c in m.getConstrs():
            if c.IISConstr:
                if debug: print('%s' % c.constrName)
                if debug: print('')
        return None
    elif m.status == GRB.Status.UNBOUNDED:
        if debug: print('Model is unbounded')
        return None
#    elif m.status == GRB.Status.INF_OR_UNBD:
#        if debug: print('Model is infeasible or unbounded')
#        return None
    else:
        if debug: print('Optimization ended with status %d' % model.status)
        return None



result=solve_example_1(5,2,3,5,10,12,3,4)
print()
if result != None:
    print("Objective=",result[0])
    print("x=",result[1])
    print("y=",result[2])
    print("d1=",result[3])
    print("d2=",result[4])