#!/usr/bin/env python
# coding: utf-8

# In[52]:


# -*- coding: utf-8 -*-

from gurobipy import *
from itertools import product
import numpy as np
import time
   
jobs = range(10)
p = [7,3,10,8,5,12,7,14,6,15]
w = [2,10,5,5,3,10,10,4,7,8]
pairs = list(product(jobs, jobs))
#for j in jobs:
    #pairs.remove((j,j))

IPmod = Model("sequence")

x = IPmod.addVars(pairs, vtype=GRB.BINARY, name="x")
#vars=[]
#for i in jobs:
    #vars.append([])
    #for j in jobs:
        #vars[i].append(IPmod.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}"))

IPmod.setObjective(quicksum(w[j]*p[i]*x[i,j] for (i,j) in pairs), GRB.MINIMIZE)

for (i,j) in pairs:
    if i<j:
        IPmod.addConstr(x[i,j] + x[j,i] == 1)

for (i,j) in pairs:
    for k in set(jobs) - {i,j}:
        IPmod.addConstr(x[i,j] + x[j,k] + x[k,i] >= 1)
        
for j in [1,2,3,4,5,6,7,8,9]:
    IPmod.addConstr(x[0,j]== 1)

for j in [4,5,7,8,9]:
    IPmod.addConstr(x[1,j]== 1)
for j in [3,5,6,7,9]:
    IPmod.addConstr(x[2,j]== 1)
for j in [7,9]:
    IPmod.addConstr(x[3,j]== 1)
for j in [7,8]:
    IPmod.addConstr(x[4,j]== 1)
for j in [6,9]:
    IPmod.addConstr(x[5,j]== 1)
IPmod.addConstr(x[7,9]== 1)
for i in jobs:
    IPmod.addConstr(x[i,i]== 1)
IPmod.optimize()


xsol=[]
xsol= IPmod.getAttr('x', x)
if IPmod.status == GRB.OPTIMAL:
    print("Optimal Assignment:")
    for (i,j) in pairs:
        if x[i,j].x > 0.5:
            print(f"Job {i} is finished ealier job {j}")
    print("Completion Time:", IPmod.objVal)
else:
    print("No solution found")


                     


# In[ ]:




