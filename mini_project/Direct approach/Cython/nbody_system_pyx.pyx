import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"


import numpy as np
cimport numpy as np
cimport cython


np.import_array()

cdef class body:

    cdef:
        int name               
        double mass, radius, x, y, z, vx, vy, vz

    def __init__(self, n_system):
        self.name = int(n_system[0])            #Name of the body
        self.mass = float(n_system[1])            #Mass of the body   (kg)
        self.radius = float(n_system[2])

        self.x = float(n_system[3])               #x position         (km)
        self.y = float(n_system[4])                 #y position         (km)
        self.z = float(n_system[5])                 #z position         (km)

        self.vx = float(n_system[6])                #x velocity         (km/s)
        self.vy = float(n_system[7])                #y velocity         (km/s)
        self.vz = float(n_system[8])                #z velocity         (km/s)

    cdef void update(self, int timestep, np.ndarray acceleration):
        cdef:
            double ax, ay, az               #Acceleration       (km/s)
            double new_vx, new_vy, new_vz   #New velocities     (km/s)
            double new_x, new_y, new_z      #New positions      (km)

        self.ax = acceleration[0]
        self.ay = acceleration[1] 
        self.az = acceleration[2] 

        #v_i_new = v_i + (a_i * t)
        new_vx = self.vx + (self.ax * timestep)
        new_vy = self.vy + (self.ay * timestep)
        new_vz = self.vz + (self.az * timestep)

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

    cdef public position(self):
        cdef np.ndarray pos = np.array([self.x, self.y, self.z])
        return pos
    
    def draw(self, ax):
        ax.scatter(self.x, self.y, self.z, label=self.name)
        


cdef class system:

    cdef:
        int bodycount
        int nbody
        object[:] bodies

    def __init__(self, nbody):
        self.bodycount = 0
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=object)

    def __repr__(self):
        return f"[]"

    cdef void insert(self, object body):
        if self.bodycount < self.nbody:
            self.bodies[self.bodycount] = body
            self.bodycount += 1
        else:
            print("System reached maxmimum, body not added")

    cdef void update(self, int timestep):
        cdef:
            int count
            double G_const
            np.ndarray acceleration, a_array, a_i, r1, r2, r_diff

        print("update(self, int %s)" % timestep)
        
        G_const = 6.67430E-11
        for body1 in self.bodies:
            count = 0
            a_array = np.zeros(((self.nbody-1), 3), dtype=object)     #Acceleration array (m/s)
            for body2 in self.bodies:
                if (body1 is not body2):
                    print("body1 %s , body2 %s " % (body1, body2))

                    r1 = np.array([body1[3], body1[4], body1[5]])
                    r2 = np.array([body2[3], body2[4], body2[5]])
                    print("r1 r2")
                    r_diff = np.array([body1[3]-body2[3], body1[4]-body2[4], body1[5]-body2[5]])
                    print("r_diff %s " % r_diff)
                    a_i = -1*G_const*((body2[1]*r_diff) / np.power(np.absolute(r_diff), 3))

                    a_array[count] = a_i
                    count += 1
            acceleration = np.sum(a_array, axis=0, dtype=np.double)

            body1.update(timestep, acceleration)
            print("body1.update works")
            

    def run(self, timestep, steps, display=False):
        cdef:
            Py_ssize_t i
        
        for i in range(steps):
            self.update(timestep)



def main(timestep, steps):
    cdef:
        Py_ssize_t i
        int nbody

    solar_system = np.loadtxt("system.csv", skiprows=2, delimiter=',', dtype=np.float64)

    nbody = int(len(solar_system))
    ssystem = system(nbody)
    print("OK")

    #for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
    #    body_data = body(name, mass, radius, x, y, z, vx, vy, vz)
    #    ssystem.insert(body_data)
    print("OK2")
    for i in range(nbody):
        print("OK %s" % i)

        ssystem.insert(solar_system[i])
    print("ALL INSERTED")

    ssystem.run(timestep, steps, False)
    print("END")