from gurobipy import * #Calls Gurobi Package

#define our solve_model function
def solve_example_1(a1x,a1y,a2x,a2y,b1,b2,cx,cy):
    #Model Definition

    #Variables Definition
    
    #Constraint Definition

    #Objective Function

    #Solve!

    #Return appropriate info depending on model status: 
    if m.status == GRB.Status.OPTIMAL:
        
    elif m.status == GRB.Status.INFEASIBLE:
        
    elif m.status == GRB.Status.UNBOUNDED:
    
    else:

result=solve_example_1(5,2,3,5,10,12,3,4)
if result != None:
    print("Objective=",result[0])
    print("x=",result[1])
    print("y=",result[2])
    print("d1=",result[3])
    print("d2=",result[4])