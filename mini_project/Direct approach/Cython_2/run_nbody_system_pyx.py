import sys
from nbody_system_pyx import main
import time


if int(len(sys.argv)) == 3:
    start_time = time.time()
    main(int(sys.argv[1]), int(sys.argv[2]))
    execution_time = (time.time() - start_time)
    print("Execution time: {:.4f} s".format(execution_time))
    print("Timestep: {} s \nStep: {} \n10 bodies".format(int(sys.argv[1]), int(sys.argv[2])))
elif int(len(sys.argv)) == 4:
    start_time = time.time()
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    execution_time = (time.time() - start_time)
    print("Timestep: {} s \nStep: {} \n{} bodies".format(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))
    print("Execution time: {:.4f} s".format(execution_time))
else:
    print("Usage: python {} <TIMESTEP> <ITERATIONS>".format(sys.argv[0]))
