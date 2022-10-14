#
# mpi_scatter.py
#
# Simple demonstration of scatter method.
#
# Run by typing:
# mpirun -np 4 python mpi_scatter.py
#

from mpi4py import MPI
import numpy as np

SIZE=4
sendbuf=np.zeros((SIZE,SIZE))
recvbuf=np.zeros(SIZE)
    
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numtasks = comm.Get_size()

if numtasks==SIZE:
    # define source task and elements to send/receive,
    # then perform collective scatter
    source = 2
    sendcount = SIZE
    recvcount = SIZE
    # only the source task initialises sendbuf
    if rank==source:
        for i in range(SIZE):
            for j in range(SIZE):
                sendbuf[i,j] = i*SIZE + j+1
    # all ranks issue MPI_Scatter command
    recvbuf=comm.scatter(sendbuf,root=source)

    print("rank= {:2d} Results: {:4.1f} {:4.1f} {:4.1f} {:4.1f}".format(rank,recvbuf[0],recvbuf[1],recvbuf[2],recvbuf[3]))
else:
    print("Must specify",SIZE," processors. Terminating.")
