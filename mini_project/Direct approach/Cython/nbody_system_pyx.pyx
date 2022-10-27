import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

cimport numpy as np
cimport matplotlib.pyplot as plt
cimport matplotlib.animation as animation


cdef class body:
    cdef __init__(self, name, mass, x, y, z, vx, vy, vz):
        cdef:
            char self.name = name            #Name of the body
            double self.mass = mass            #Mass of the body   (kg)

            double self.x = x                  #x position         (km)
            double self.y = y                  #y position         (km)
            double self.z = z                  #z position         (km)

            double self.vx = vx                #x velocity         (km/s)
            double self.vy = vy                #y velocity         (km/s)
            double self.vz = vz                #z velocity         (km/s)

    cdef update(self, timestep, acceleration):
        cdef:
            double self.ax = acceleration[0]
            double self.ay = acceleration[1] 
            double self.az = acceleration[2] 

        #v_i_new = v_i + (a_i * t)
            double new_vx = self.vx + (self.ax * timestep)
            double new_vy = self.vy + (self.ay * timestep)
            double new_vz = self.vz + (self.az * timestep)

        #r_i = r_i + (v_i * t)
            double new_x = self.x + (new_vx * timestep)
            double new_y = self.y + (new_vy * timestep)
            double new_z = self.z + (new_vz * timestep)

        #Write new positions
            double self.x = new_x
            double self.y = new_y
            double self.z = new_z

        #Write new velocities
            double self.vx = new_vx
            double self.vy = new_vy
            double self.vz = new_vz

    def position(self):
        return np.array([self.x, self.y, self.z])
    
    def draw(self, ax):

        ax.scatter(self.x, self.y, self.z, label=self.name)
        


class system:
    bodycount = 0
    def __init__(self, nbody):
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=object)

    def __repr__(self):
        return f"[]"

    def insert(self, body):
        if self.bodycount < self.nbody:
            self.bodies[self.bodycount] = body
            self.bodycount += 1
        else:
            print("System reached maxmimum, body not added")

    def update(self, timestep):
        cdef:
        int count
            double G_const
            double[:,:] acceleration, a_array 
            double[:] a_i, r1, r2, r_diff
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

        for step in range(0, steps):
            self.update(timestep)
            if (display == True):
                fig = plt.figure()
                ax = plt.axes(projection = '3d')
                self.display(ax)
                save = "%s.png" % step
                plt.savefig(save)
                


            


    def display(self, ax):
        for body in self.bodies:
            body.draw(ax)



def main(timestep, steps)
    file_name = r"mini_project\Direct approach\Cython\system.csv"
    df = pd.read_csv(file_name, header=1)
    solar_system = np.array(df)

    nbody = len(solar_system)
    ssystem = system(nbody) 

    for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
        body_data = body(name, mass, x, y, z, vx, vy, vz)
        ssystem.insert(body_data)

    ssystem.run(timestep, steps, False)
