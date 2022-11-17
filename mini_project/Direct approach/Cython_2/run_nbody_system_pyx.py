import sys
from nbody_system_pyx import main
import time


if int(len(sys.argv)) == 4:
    start_time = time.time()
    print("Start {}".format(start_time))
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    execution_time = (time.time() - start_time)
    print("Timestep: {} s \nSteps: {} \n{} bodies".format(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))
    print("Execution time: {:.4f} s".format(execution_time))
else:
    print("Usage: python {} <TIMESTEP> <ITERATIONS> <BODIES>".format(sys.argv[0]))
