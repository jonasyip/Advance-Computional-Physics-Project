//------------------Prime Number Counter----------------
# include <math.h>
# include <mpi.h>
# include <stdio.h>
# include <stdlib.h>
# include <time.h>

int main ( int argc, char *argv[] );
int prime_number ( int n, int id, int p );

int main ( int argc, char *argv[] ){
    int i, id, ierr, n, n_factor=2, p;
    int n_lo=1, n_hi=65536;
    int primes, primes_part;
    double wtime;
    
    ierr = MPI_Init ( NULL, NULL );
    ierr = MPI_Comm_size ( MPI_COMM_WORLD, &p );
    ierr = MPI_Comm_rank ( MPI_COMM_WORLD, &id );
    
    if ( id == 0 ){
        printf ( "PRIME_MPI\n" );
        printf ( "  C/MPI version\n" );
        printf ( "  MPI  program to count primes.\n" );
        printf ( "  Number of processes is %d\n", p );
        printf ( "         N      Primes      Time\n" );
    }
    
    n = n_lo;
    while ( n <= n_hi ){
        if ( id == 0 ){
            wtime = MPI_Wtime ( );
        }
        ierr = MPI_Bcast ( &n, 1, MPI_INT, 0, MPI_COMM_WORLD );
        primes_part = prime_number ( n, id, p );
        ierr = MPI_Reduce ( &primes_part, &primes,
                           1, MPI_INT, MPI_SUM, 0,
                           MPI_COMM_WORLD );
        
        if ( id == 0 ) {
            wtime = MPI_Wtime ( ) - wtime;
            printf ( "  %8d  %8d  %14f\n", n, primes, wtime );
        }
        n = n * n_factor;
    }
    ierr = MPI_Finalize ( );
    
    if ( id == 0 ) {
        printf ( "\n");
        printf ( "PRIME_MPI - Master process:\n");
        printf ( "  Normal end of execution.\n");
        printf ( "\n" );
    }
    return 0;
}

int prime_number ( int n, int id, int p ){
    int i, j, prime, total=0;
    for ( i = 2 + id; i <= n; i = i + p ){
        prime = 1;
        for ( j = 2; j < i; j++ ){
            if ( ( i % j ) == 0 ){
                prime = 0;
                break;
            }
        }
        total += prime;
    }
    return total;
}
