import sys
from openmp_nbody_system_pyx import main

if int(len(sys.argv)) == 5:
    main(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

elif int(len(sys.argv)) == 6:
    main(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), str(sys.argv[5]))
else:
    print("Usage: python {} <TIMESTEP> <ITERATIONS> <NBODIES> <THREADS> <(COMMENTS)>".format(sys.argv[0]))
