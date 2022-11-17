import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from nbody_system import system, body
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import time


file_name = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python\initial_conditions.csv"
df = pd.read_csv(file_name, header=1)
nbody_system = np.array(df)[0:20]


nbody = len(nbody_system)

steps = 200
timestep = 1.037e+6

ssystem = system(nbody, steps) 

# for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
for name, mass, x, y, z, vx, vy, vz in nbody_system:
    body_data = body(name, mass, x, y, z, vx, vy, vz)
    ssystem.insert(body_data)
    
start_time = time.time()
ssystem.run(timestep, steps, False)
execution_time = (time.time() - start_time)
print("Execution time: {:.2f}".format(execution_time))
print("Done")
