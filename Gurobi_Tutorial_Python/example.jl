using JuMP,Gurobi # we are using packages JuMP and Gurobi
const MOI = JuMP.MathOptInterface
m = Model(with_optimizer(Gurobi.Optimizer))
# create a model named m and we are using Gurobi to solve it

@variable(m,x>=0)
@variable(m,y>=0)
# create two nonnegative variables x,y and associate them with model m

@objective(m,Max,3x+4y)
# create a maximization objective function and associate it with model m

m1=@constraint(m,5x+2y<=10)
m2=@constraint(m,3x+5y<=12)
# create constraints and associate them with model m

print(m) # print out the model

status=optimize!(m) # Solve the model

println("Objective value: ",JuMP.objective_value(m))
println("x = ",JuMP.value(x))
println("y = ",JuMP.value(y))
println("dual m1=",JuMP.dual(m1))
println("dual m2=",JuMP.dual(m2))
