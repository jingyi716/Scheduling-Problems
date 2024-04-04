#!/usr/bin/env python
# coding: utf-8

# In[18]:


import gurobipy as gp
from gurobipy import GRB
#COded by Juan Estrada 
# Sample cost matrix (replace this with your actual cost matrix)
cost_matrix = [
    [0,5,5,5,5,5,5],
    [0,4,4,4,4,4,4],
    [0,4,4,4,4,4,4],
    [0,0,8,8,8,8,8],
    [0,0,0,5,5,5,5],
    [0,0,0,3,3,3,3],
    [0,0,0,0,7,7,7]
]

num_tasks = len(cost_matrix)
num_workers = len(cost_matrix[0])

# Create a Gurobi model
model = gp.Model("assignment_problem")

# Create binary decision variables for the assignment
assignment_vars = []
for i in range(num_tasks):
    assignment_vars.append([])
    for j in range(num_workers):
        assignment_vars[i].append(model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")) #Task i performed by worker j

# Set objective: minimize total cost
model.setObjective(
    gp.quicksum(cost_matrix[i][j] * assignment_vars[i][j] for i in range(num_tasks) for j in range(num_workers)),
    GRB.MINIMIZE
)

# Each task must be assigned to exactly one position
for i in range(num_tasks):
    model.addConstr(gp.quicksum(assignment_vars[i][j] for j in range(num_workers)) == 1)

# Each position for  one task
for j in range(num_workers):
    model.addConstr(gp.quicksum(assignment_vars[i][j] for i in range(num_tasks)) == 1)

# Optimize the model
model.optimize()

# Print the optimal assignment and total cost
if model.status == GRB.OPTIMAL:
    print("Optimal Assignment:")
    for i in range(num_tasks):
        for j in range(num_workers):
            if assignment_vars[i][j].x > 0.5:
                print(f"Task {i} is assigned to Worker {j} with cost {cost_matrix[i][j]}")
    print("Total Cost:", model.objVal)
else:
    print("No solution found")


# In[ ]:





# In[ ]:





# In[ ]:




