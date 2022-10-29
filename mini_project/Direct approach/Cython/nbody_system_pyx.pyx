import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"


import numpy as np
cimport numpy as np
cimport cython

import pandas as pd

np.import_array()

cdef class body:

    cdef:
        char name               #Name of the body
        double mass, x, y, z, vx, vy, vz

    def __init__(self, name, mass, x, y, z, vx, vy, vz):
        self.name = name            #Name of the body
        self.mass = mass            #Mass of the body   (kg)

        self.x = x                  #x position         (km)
        self.y = y                  #y position         (km)
        self.z = z                  #z position         (km)

        self.vx = vx                #x velocity         (km/s)
        self.vy = vy                #y velocity         (km/s)
        self.vz = vz                #z velocity         (km/s)

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

    cdef np.ndarray position(self):
        cdef np.ndarray pos = np.array([self.x, self.y, self.z])
        return pos
    
    def draw(self, ax):
        ax.scatter(self.x, self.y, self.z, label=self.name)
        


cdef class system:

    cdef:
        int bodycount
        int nbody
        np.ndarray bodies
        
    bodycount = 0

    def __init__(self, nbody):
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=object)

    def __repr__(self):
        return f"[]"

    cdef void insert(self, body):
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
        G_const = 6.67430E-11
        for body1 in self.bodies:
            count = 0
            a_array = np.zeros(((self.nbody-1), 3), type=np.float64)     #Acceleration array (m/s)
            for body2 in self.bodies:
                if (body1 is not body2):
                    r1 = body1.position()
                    r2 = body2.position()
                    r_diff = r1 - r2
                    a_i = -1*G_const*((body2.mass*r_diff) / np.power(np.absolute(r_diff), 3))

                    a_array[count] = a_i
                    count += 1
            acceleration = np.sum(a_array, axis=0, type=np.double)

            body1.update(timestep, acceleration)
            

    def run(self, timestep, steps, display=False):

        self.update(timestep)
        # for step in range(0, steps):
        #     self.update(timestep)
        #     if (display == True):
        #         fig = plt.figure()
        #         ax = plt.axes(projection = '3d')
        #         self.display(ax)
        #         save = "%s.png" % step
        #         plt.savefig(save)
                


            


    def display(self, ax):
        for body in self.bodies:
            body.draw(ax)



def main(timestep, steps):
    cdef:
        int nbody
        char name
        double mass, radius, x, y, z, vx, vy, vz

    file_name = r"mini_project\Direct approach\Cython\system.csv"
    df = pd.read_csv(file_name, header=1)
    solar_system = np.array(df)

    nbody = len(solar_system)
    ssystem = system(nbody)

    for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
        body_data = body(name, mass, x, y, z, vx, vy, vz)
        ssystem.insert(body_data)

    ssystem.run(timestep, steps, False)
