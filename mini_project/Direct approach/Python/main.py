import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from nbody_system import system, body
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import time

def main(timestep, steps, nbodies, comment=None):

    if comment is None:
        comment = ""

    file_name = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python\initial_conditions.csv"
    df = pd.read_csv(file_name, header=1)
    nbody_system = np.array(df)[0:nbodies]


    nbody = len(nbody_system)

    steps = 200
    timestep = 1.037e+6

    nbody_system = system(nbody, steps) 

    # for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
    for name, mass, x, y, z, vx, vy, vz in nbody_system:
        body_data = body(name, mass, x, y, z, vx, vy, vz)
        nbody_system.insert(body_data)
        

    print("\nnbody_system.py")
    print("==========================")
    start_time = time.time()
    nbody_system.run(timestep, steps)
    end_time = time.time()
    nbody_system.sframes.save()
    execution_time = (end_time - start_time)
    print("Start {}".format(time.ctime(int(start_time))))
    print("End   {}".format(time.ctime(int(end_time))))
    print("Timestep: {} s \nSteps: {} \n{} bodies".format(timestep, steps, nbodies))
    print("Execution time: {:.4f} s".format(execution_time))

    #start_time,end_time,timestep,steps,bodies,threads,execution_time
    omp_execution_history = "{},{},{},{},{},{},{}".format(time.ctime(int(start_time)), time.ctime(int(end_time)), 
                                                timestep, steps, nbodies, execution_time, comment)
    f=open('python_execution_history.csv','a')
    f.write("\n")
    f.write(omp_execution_history)
    f.close()