import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"


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
        #print("inserted")
    
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

        self.x = x                  #x position         (km)
        self.y = y                  #y position         (km)
        self.z = z                  #z position         (km)

        self.vx = vx                #x velocity         (km/s)
        self.vy = vy                #y velocity         (km/s)
        self.vz = vz                #z velocity         (km/s)
    
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
        int nbody, bodycount
        public object sframes


    def __init__(self, nbody, steps):
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=body)
        self.bodycount = 0

    cpdef void insert(self, body body):
        if self.bodycount < self.nbody:
            self.bodies[self.bodycount] = body
            self.bodycount += 1
        else:
            print("System reached maxmimum, body not added")

    cpdef void update(self, double timestep):
        cdef:
            double G_CONST
            np.ndarray a_to_update, r1, r2, r_diff, a_i, acceleration
            int count, count_j


        G_CONST = 6.67430E-11

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
                    a_i = -1*G_CONST*((body2.mass*r_diff) / np.power(np.absolute(r_diff), 3))

                    a_array[count] = a_i
                    count += 1
            acceleration = np.sum(a_array, axis=0, dtype=np.float64)
            a_to_update[count_j] = acceleration
            count_j += 1

        for count, body1, accel in zip(range(self.nbody), self.bodies, a_to_update):
            body1.update(timestep, accel)

        self.sframes.insert(self.bodies)


    def run(self, timestep, steps, display=False):
        
        self.sframes = frames(steps+1)
        self.sframes.insert(self.bodies)
        for step in range(0, steps):
            self.update(timestep)

        self.sframes.save()



def main(timestep, steps, nbodies=10):
    cdef:
        Py_ssize_t i
        int nbody
        n_system nbody_system
        body body_data
        np.ndarray initial

    initial = np.loadtxt("initial_conditions.csv", skiprows=2, delimiter=',', dtype=np.float64)
    initial = initial[0:nbodies]
    nbody = int(len(initial))
    nbody_system = n_system(nbody, steps)
    print("OK")

    #for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
    #    body_data = body(name, mass, radius, x, y, z, vx, vy, vz)
    #    ssystem.insert(body_data)
    print("OK2")
    for i in range(nbody):
        print("OK %s" % i)
        body_data = body(*initial[i])
        nbody_system.insert(body_data)
    print("ALL INSERTED")

    nbody_system.run(timestep, steps, False)
    print("END")