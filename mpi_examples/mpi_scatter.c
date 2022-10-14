//
// mpi_scatter.c
//
// Simple demonstration of scatter method.
//
#include <mpi.h>
#include <stdio.h>
#define SIZE 4

int main(){
    int numtasks, rank, sendcount, recvcount, source;
    double sendbuf[SIZE][SIZE];
    double recvbuf[SIZE];
    
    MPI_Init(NULL,NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
    
    if (numtasks == SIZE) {
        // define source task and elements to send/receive,
        // then perform collective scatter
        source = 2;
        sendcount = SIZE;
        recvcount = SIZE;
        // only the source task initialises sendbuf
        if (rank==source)
            for (int i=0; i<SIZE; i++)
                for (int j=0; j<SIZE; j++)
                    sendbuf[i][j] = i*SIZE + j+1;
        // all ranks issue MPI_Scatter command
        MPI_Scatter(sendbuf,sendcount,MPI_DOUBLE,recvbuf,recvcount,
                    MPI_DOUBLE,source,MPI_COMM_WORLD);
        
        printf("rank= %d  Results: %f %f %f %f\n",rank,recvbuf[0],
               recvbuf[1],recvbuf[2],recvbuf[3]);
    }
    else
    printf("Must specify %d processors. Terminating.\n",SIZE);
    MPI_Finalize();
}