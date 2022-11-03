import sys
from nbody_system_pyx import main


if int(len(sys.argv)) == 3:
    main(int(sys.argv[1]), int(sys.argv[2]))
elif int(len(sys.argv)) == 4:
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
else:
    print("Usage: python {} <TIMESTEP> <ITERATIONS>".format(sys.argv[0]))
