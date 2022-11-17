#=====================
# nbody_system_pyx.pyx
#  (Cython)
#=====================

import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import time
import numpy as np
cimport numpy as np
cimport cython



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
            data = np.array([star.name, star.mass, star.x, star.y, star.z, star.vx, star.vy, star.vz])
            star_data[i] = data

        self.system_frames[self.frame_count] = star_data
        self.frame_count += 1
    
    cpdef void save(self):
        cdef:
            str path, savename, savepath

        path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Cython_2"
        savename = "frames_pyx.npy"
        savepath = "%s\%s" % (path, savename)
        np.save(savepath, self.system_frames)



cdef class body:
    cdef public double name, mass, x, y, z, vx, vy, vz

    def __init__(self, name, mass, x, y, z, vx, vy, vz):

        self.name = name            #Name of the body
        self.mass = mass            #Mass of the body   (kg)

        self.x = x                  #x position         (m)
        self.y = y                  #y position         (m)
        self.z = z                  #z position         (m)

        self.vx = vx                #x velocity         (m/s)
        self.vy = vy                #y velocity         (m/s)
        self.vz = vz                #z velocity         (m/s)
    
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

    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef np.ndarray position(self):
        cdef np.ndarray pos

        pos = np.array([self.x, self.y, self.z])
        return pos


cdef class n_system:
    cdef:
        np.ndarray bodies
        int nbody, bodycount
        public frames sframes
        public double G_CONST


    def __init__(self, nbody, steps):
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=body)
        self.bodycount = 0

        self.G_CONST = 6.67430E-11

    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef void insert(self, body body):
        if self.bodycount < self.nbody:
            self.bodies[self.bodycount] = body
            self.bodycount += 1
        else:
            print("System reached maxmimum, body not added")

    @cython.wraparound(False)
    @cython.boundscheck(False)
    cpdef void update(self, double timestep):
        cdef:
            
            np.ndarray a_to_update, r1, r2, r_diff, a_i, acceleration
            int count, count_j


        

        a_to_update = np.zeros(self.nbody, dtype=object)
        count_j = 0
        for body1 in self.bodies:
            count = 0
            a_array = np.zeros(((self.nbody-1), 3))     #Acceleration array (m/s)
            for body2 in self.bodies:
                if (body1 is not body2):
                    r1 = body1.position()
                    r2 = body2.position()
                    r_diff = r1 - r2
                    a_i = -1*self.G_CONST*((body2.mass) / np.power(np.linalg.norm(r_diff), 2)) * (r_diff / np.linalg.norm(r_diff))
                    a_array[count] = a_i
                    count += 1
            acceleration = np.sum(a_array, axis=0, dtype=np.float64)
            a_to_update[count_j] = acceleration
            count_j += 1

        for body1, accel in zip(self.bodies, a_to_update):
            body1.update(timestep, accel)

        self.sframes.insert(self.bodies)


    cdef run(self, double timestep, int steps):
        cdef Py_ssize_t step
        
        self.sframes = frames(steps+1)
        self.sframes.insert(self.bodies)
        for step in range(0, steps):
            self.update(timestep)

        self.sframes.save()



def main(timestep, steps, nbodies, comment):
    cdef:
        Py_ssize_t i
        int nbody
        n_system nbody_system
        body body_data
        np.ndarray initial

    initial = np.loadtxt("initial_conditions.csv", skiprows=1, delimiter=',', dtype=np.float64)
    initial = initial[0:nbodies]
    nbody = int(len(initial))
    nbody_system = n_system(nbody, steps)

    for i in range(nbody):
        body_data = body(*initial[i])
        nbody_system.insert(body_data)

    print("\nnbody_system_pyx.pyx")
    print("==========================")
    start_time = time.time()
    nbody_system.run(timestep, steps)
    end_time = time.time()
    execution_time = (end_time - start_time)
    print("Start {}".format(time.ctime(int(start_time))))
    print("End   {}".format(time.ctime(int(end_time))))
    print("Timestep: {} s \nSteps: {} \n{} bodies".format(timestep, steps, nbodies))
    print("Execution time: {:.4f} s".format(execution_time))

    #start_time,end_time,timestep,steps,bodies,threads,execution_time
    omp_execution_history = "{},{},{},{},{},{},{}".format(time.ctime(int(start_time)), time.ctime(int(end_time)), 
                                                timestep, steps, nbodies, execution_time, comment)
    f=open('cython_execution_history.csv','a')
    f.write("\n")
    f.write(omp_execution_history)
    f.close()