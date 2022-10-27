import sys
from nbody_system_pyx import main


if int(len(sys.argv)) == 2:
    main(int(sys.argv[1]))
