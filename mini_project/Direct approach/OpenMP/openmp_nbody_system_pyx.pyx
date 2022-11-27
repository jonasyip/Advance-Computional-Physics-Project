#============================
# openmp_nbody_system_pyx.pyx
#============================

import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import time
import numpy as np
cimport numpy as np
cimport cython
from cython.parallel import parallel, prange
cimport openmp
from libc.math cimport sqrt

np.import_array()

cdef class frames:
    cdef:
        int total_frames
        public np.ndarray system_frames
        public int frame_count

    def __init__(self, total_frames):
        self.total_frames = total_frames
        self.system_frames = np.zeros(total_frames, dtype=object)
        self.frame_count = 0

    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef void insert(self, object frame):
        cdef:
            int length
            np.ndarray star_data, data
            Py_ssize_t i
            body star

        length = len(frame)
        star_data = np.zeros(length, dtype=object)
        for i, star in zip(range(length), frame):
            data = np.array([star.ID, star.mass, star.x, star.y, star.z, star.vx, star.vy, star.vz])
            star_data[i] = data

        self.system_frames[self.frame_count] = star_data
        self.frame_count += 1
    
    cpdef void save(self):
        cdef:
            str path, savename, savepath

        path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\OpenMP"
        savename = "omp_frames_pyx.npy"
        savepath = "%s\%s" % (path, savename)
        np.save(savepath, self.system_frames)



cdef class body:
    cdef public int ID
    cdef public double mass, x, y, z, vx, vy, vz

    def __init__(self, ID, mass, x, y, z, vx, vy, vz):

        self.ID = ID                #ID of the body
        self.mass = mass            #Mass of the body   (kg)

        self.x = x                  #x position         (km)
        self.y = y                  #y position         (km)
        self.z = z                  #z position         (km)

        self.vx = vx                #x velocity         (km/s)
        self.vy = vy                #y velocity         (km/s)
        self.vz = vz                #z velocity         (km/s)


    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef void update(self, double timestep, np.ndarray acceleration):
        cdef:
            double ax, ay, az               #Acceleration
            double new_vx, new_vy, new_vz   #New velocites
            double new_x, new_y, new_z      #New positions

        ax = acceleration[0]
        ay = acceleration[1] 
        az = acceleration[2] 

        #v_i_new = v_i + (a_i * t)
        new_vx = self.vx + (ax * timestep)
        new_vy = self.vy + (ay * timestep)
        new_vz = self.vz + (az * timestep)

        #r_i = r_i + (v_i * t)
        new_x = self.x + (new_vx * timestep)
        new_y = self.y + (new_vy * timestep)
        new_z = self.z + (new_vz * timestep)

        #Write new positions
        self.x = new_x
        self.y = new_y
        self.z = new_z

        #Write new velocities
        self.vx = new_vx
        self.vy = new_vy
        self.vz = new_vz

    
    cpdef np.ndarray position(self):
        cdef np.ndarray pos

        pos = np.array([self.x, self.y, self.z])
        return pos


cdef class n_system:
    cdef:
        np.ndarray bodies
        int nbody, total_bodies
        public object sframes
        int threads

    def __init__(self, nbody, steps, threads):
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=body)
        self.total_bodies = 0
        self.threads = threads

    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef void insert(self, body body):
        if self.total_bodies < self.nbody:
            self.bodies[self.total_bodies] = body
            self.total_bodies += 1
        else:
            print("System reached maxmimum, body not added")

    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef void openmp(self, double[:] x, double[:] y, double[:] z, double[:] ax, double[:] ay, double[:] az, 
    double[:] masses):
        cdef double G_CONST = 6.67430E-11

        for count_i in prange(self.nbody, nogil=True, num_threads=self.threads, schedule="static"):
            for count_j in self.nbody:
                if (count_i != count_j):
                    body2_mass = masses[count_j]
                    r_diff = sqrt((x[count_i] - x[count_j])**2 + (y[count_i] - y[count_j])**2 + (z[count_i] - z[count_j])**2)
                    ax[count_i] += -1*G_CONST*((body2_mass) / r_diff**2) * ((x[count_i] - x[count_j]) / r_diff)
                    ay[count_i] += -1*G_CONST*((body2_mass) / r_diff**2) * ((y[count_i] - y[count_j]) / r_diff)
                    az[count_i] += -1*G_CONST*((body2_mass) / r_diff**2) * ((z[count_i] - z[count_j]) / r_diff)

        for ax1, ay1, az1 in zip(ax, ay, az):
            acceleration = np.zeros(3, dtype=np.double)
            acceleration[0] = ax1
            acceleration[1] = ax2
            acceleration[2] = ax3
            body1.update(timestep, acceleration)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef void update(self, double timestep):
        cdef:
            
            int count_i
            body body1
            np.ndarray acceleration

        cdef double[:] x = np.zeros(self.nbody, dtype=np.double)
        cdef double[:] y = np.zeros(self.nbody, dtype=np.double)
        cdef double[:] z = np.zeros(self.nbody, dtype=np.double)
        cdef double[:] ax = np.zeros(self.nbody, dtype=np.double)
        cdef double[:] ay = np.zeros(self.nbody, dtype=np.double)
        cdef double[:] az = np.zeros(self.nbody, dtype=np.double)
        cdef double[:] masses = np.zeros(self.nbody, dtype=np.double) 

        for count_i, body1 in (range(self.nbody), self.bodies):
            masses[count_i] = body1.masses
            x[count_i] = body1.x
            y[count_i] = body1.y
            z[count_i] = body1.z

        G_CONST = 6.67430E-11

        self.openmp(x, y, z, ax, ay, az, masses)

        self.sframes.insert(self.bodies)

    def calculate_acceleration(self, body1, body2):
        G_CONST = 6.67430E-11
        r1 = body1.position()
        r2 = body2.position()
        r_diff = r1 - r2
        a_i = -1*G_CONST*((body2.mass) / np.power(np.linalg.norm(r_diff), 2)) * (r_diff / np.linalg.norm(r_diff))
        body1.acceleration[0] += a_i[0]
        body1.acceleration[1] += a_i[1]
        body1.acceleration[2] += a_i[2]
        


    cdef run(self, double timestep, int steps):
        cdef Py_ssize_t step
        
        self.sframes = frames(steps+1)
        self.sframes.insert(self.bodies)
        for step in range(0, steps):
            self.update(timestep)

        self.sframes.save()



def main(timestep, steps, nbodies, threads, comment=None):
    cdef:
        Py_ssize_t i
        int nbody
        n_system nbody_system
        body body_data
        np.ndarray initial

    if comment is None:
        comment = ""

    initial = np.loadtxt("initial_conditions.csv", skiprows=1, delimiter=',', dtype=np.float64)
    initial = initial[0:nbodies]
    nbody = int(len(initial))
    nbody_system = n_system(nbody, steps, threads)

    
    
    for i in range(nbody):
        body_data = body(*initial[i])
        nbody_system.insert(body_data)


    print("\nopenmp_nbody_system_pyx.pyx")
    print("===========================")
    start_time = time.time()
    nbody_system.run(timestep, steps)
    end_time = time.time() 
    execution_time = (end_time - start_time)
    print("Start {}".format(time.ctime(int(start_time))))
    print("End   {}".format(time.ctime(int(end_time))))
    print("Timestep: {} s \nSteps: {} \n{} bodies \n{} threads".format(timestep, steps, nbodies, threads))
    print("Execution time: {:.4f} s".format(execution_time))

    #start_time,end_time,timestep,steps,bodies,threads,execution_time
    omp_execution_history = "{},{},{},{},{},{},{},{}".format(time.ctime(int(start_time)), time.ctime(int(end_time)), 
                                                timestep, steps, nbodies, threads, execution_time, comment)
    f=open('omp_execution_history.csv','a')
    f.write("\n")
    f.write(omp_execution_history)
    f.close()