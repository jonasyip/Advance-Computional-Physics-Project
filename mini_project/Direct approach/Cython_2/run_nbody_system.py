import sys
from nbody_system_pyx import main
import time


if int(len(sys.argv)) == 4: #Without comments
    main(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
elif int(len(sys.argv)) == 5: #With comments
    main(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), str(sys.argv[4]))
else:
    print("Usage: python {} <TIMESTEP> <ITERATIONS> <NBODIES> <(COMMENTS)>".format(sys.argv[0]))
