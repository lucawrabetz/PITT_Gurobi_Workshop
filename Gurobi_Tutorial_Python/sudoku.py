import time
from gurobipy import *
import os
import numpy as np

def read_sudoku_file(filename):
    # Read Data from file
    f = open(filename)
    grid=[]
    l=f.readlines();
    for (i,ln) in enumerate(l):
        row=ln.replace(" \n","").split(" ");
        grid.append([]);
        for j in range(len(row)):
            grid[i].append(int(row[j]));
    f.close()
    
    s = sum([len(S) for S in grid]);#len(grid[0])
    print(s)
    return None
    n = int(s**0.5); # n is 9
    
    # Fix variables associated with cells whose values are pre-specified
    A=[];b=[];
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0:
                v = int(grid[i][j]) - 1
                l=len(A)
                A+=[[0 for k in range(n**3)]]
                A[l][i*n**2 + j*n + v]=1;b+=[1]
    
    # Each cell must take one value
    for i in range(n):
        for j in range(n):
            l=len(A);
            A+=[[0 for k in range( n**3)]]
            b+=[1]
            for k in range(n):
                A[l][i * n**2 + j * n + k]=1
    
    # Each value appears once per row
    for i in range(n):
        for j in range(n):
            l=len(A);
            A+=[[0 for k in range( n**3)]]
            b+=[1]
            for k in range(n):
                A[l][j * n**2 + k * n + i]=1
    
    # Each value appears once per column
    for i in range(n):
        for j in range(n):
            l=len(A);
            A+=[[0 for k in range( n**3)]]
            b+=[1]
            for k in range(n):
                A[l][k * n**2 + i * n + j]=1
    
    # Each value appears once per subgrid
    n05=int(n**0.5);
    for i1 in range(n05):
        for j1 in range(n05):
            for k in range(n):
                l=len(A)
                A+=[[0 for m in range( n**3)]]
                b+=[1]
                for i2 in range(i1*n05,(i1+1)*n05):
                    for j2 in range(j1*n05,(j1+1)*n05):
                        A[l][i2 * n**2 + j2 * n + k]=1
    return A,b

###################################################################################
###################################################################################
###################################################################################

def solRELX_Ax_e_b(A,b,c,j,debug):
    #x is restricted positive, problem is maximization
    
    # Create variables and constraints
    
    t=time.time()
    m.optimize();
    t=time.time()-t;
    if m.status == GRB.Status.OPTIMAL:
        if debug: print('Optimal objective: %g' % m.objVal)
        
    elif m.status == GRB.Status.INF_OR_UNBD:
        if debug: print('Model is infeasible or unbounded')
        return None
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
    else:
        if debug: print('Optimization ended with status %d' % model.status)
        return None

###################################################################################
###################################################################################
###################################################################################

tm=[]
debug=0
for i in range(100):
    A,b=read_sudoku_file("dat/"+str(i+1)+"-Sudoku.txt")
    resuts=solRELX_Ax_e_b(A,b,[0 for i in range(len(A[0]))],i,debug);
    if resuts==None: continue;
    x,t=resuts;
    tm.append(t);
    if debug:
        n=9;
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if x[i * n**2 + j * n + k]>0.99:
                        if j%3==0 and j!=0:
                            print("|",end="")
                        print("|",k+1,end="")
                if len([x[i * n**2 + j * n + k] for k in range(n) if 0.01<
                        x[i * n**2 + j * n + k] and x[i * n**2 + j * n + k]<0.99])>0:
                    if j%3==0 and j!=0:
                        print("|",end="")
                    print("|",0,end="")
            print("|",end=".")
            print("");
            if (i+1)%3==0 and i!=0:
                print("---------------------------------")

###################################################################################
###################################################################################
###################################################################################

ttm=[]
for i in range(100):
    model = read(os.getcwd()+"/models/out"+str(i+1)+".lp");
    model.setParam( 'OutputFlag', debug)
#    model.setParam( 'tuneResults', 1)
    # Set the TuneResults parameter to 1
    model.Params.tuneResults = 1
    # Tune the model
    model.tune()
    if model.tuneResultCount > 0:
        # Load the best tuned parameters into the model
        model.getTuneResult(0)    
        # Write tuned parameters to a file
        model.write("tuned/tune"+str(i+1)+".prm")
        # Solve the model using the tuned parameters
        t=time.time()
        model.optimize()
        ttm.append(time.time()-t);

print("Average solution time=",np.mean(tm)/60," minutes.");
print("Average (tuned) solution time=",np.mean(ttm)/60," minutes.");


  
