import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import sys
import time

class frames:
    def __init__(self, total_frames):
        self.total_frames = total_frames
        self.system_frames = np.zeros(total_frames, dtype=object)
        self.frame_count = 0

    def insert(self, frame):
        """
        Inserts a snapshot of the nbody system (system object).

        Parameters
        ----------
        frame : system
            System object

        """
        length = len(frame) 
        star_data = np.zeros(length, dtype=object)
        for i, star in zip(range(length), frame):
            data = np.array([star.name, star.mass, star.x, star.y, star.z, star.vx, star.vy, star.vz])
            star_data[i] = data

        self.system_frames[self.frame_count] = star_data
        self.frame_count += 1
    
    def save(self):
        """
        Saves all the system frames as a .npy
        """
        path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python"
        savename = "frames.npy"
        savepath = "%s\%s" % (path, savename)
        np.save(savepath, self.system_frames)


class body:
    def __init__(self, name, mass, x, y, z, vx, vy, vz):

        self.name = name            #Name of the body
        self.mass = mass            #Mass of the body   (kg)

        self.x = x                  #x position         (km)
        self.y = y                  #y position         (km)
        self.z = z                  #z position         (km)

        self.vx = vx                #x velocity         (km/s)
        self.vy = vy                #y velocity         (km/s)
        self.vz = vz                #z velocity         (km/s)

    def update(self, timestep, acceleration):
        """
        Updates the body position and velocity

        Parameters
        ----------
        timestep : float
            Time step

        acceleration : ndarray
            Acceleration

        """
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

    def position(self):
        """
        Returns the position of the body

        Returns
        -------
        position : ndarray
            Position of the body
        """
        return np.array([self.x, self.y, self.z])
    


class n_system:

    def __init__(self, nbody):
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=object)
        self.bodycount = 0

    def insert(self, body):
        """
        Inserts a body the nbody system

        Parameters
        ----------
        body : body
            Body object
        """
        if self.bodycount < self.nbody:
            self.bodies[self.bodycount] = body
            self.bodycount += 1
        else:
            print("System reached maxmimum, body not added")

    def update(self, timestep):
        """
        Updates the nbody system by t timestep

        Parameters
        ----------
        timestep : float
    
        """
        G_CONST = 6.67430E-11
        a_to_update = np.zeros(self.nbody, dtype=object)
        count_j = 0

        for body1 in self.bodies:
            count = 0
            acceleration = np.zeros(3, dtype=np.float64)     #Acceleration array (m/s)
            for body2 in self.bodies:
                if (body1 is not body2):
                    r1 = body1.position()
                    r2 = body2.position()
                    r_diff = r1 - r2
                    a_i = -1*G_CONST*((body2.mass) / np.power(np.linalg.norm(r_diff), 2)) * (r_diff / np.linalg.norm(r_diff))
                    acceleration = np.add(acceleration, a_i)
                    count += 1
            a_to_update[count_j] = acceleration
            count_j += 1

        for body1, accel in zip(self.bodies, a_to_update):
            body1.update(timestep, accel)

        self.sframes.insert(self.bodies)

    def run(self, timestep, steps):
        
        self.sframes = frames(steps+1)
        self.sframes.insert(self.bodies)
        for step in range(0, steps):
            self.update(timestep)

        self.sframes.save()

def main(timestep, steps, nbodies, comment=None):
    if comment is None:
        comment = ""

    initial = np.loadtxt("initial_conditions.csv", skiprows=1, delimiter=',', dtype=np.float64)
    initial = initial[0:nbodies]
    nbody = int(len(initial))
    nbody_system = n_system(nbody)

    for name, mass, x, y, z, vx, vy, vz in initial:
        body_data = body(name, mass, x, y, z, vx, vy, vz)
        nbody_system.insert(body_data)

    print("\nnbody_system.py")
    print("==========================")
    start_time = time.time()
    nbody_system.run(timestep, steps)
    end_time = time.time()
    execution_time = (end_time - start_time)
    print("Start {}".format(time.ctime(int(start_time))))
    print("End   {}".format(time.ctime(int(end_time))))
    print("Timestep: {} s \nSteps: {} \n{} bodies \nComment: {}".format(timestep, steps, nbodies,comment))
    print("Execution time: {:.4f} s".format(execution_time))

    #start_time,end_time,timestep,steps,bodies,threads,execution_time
    omp_execution_history = "{},{},{},{},{},{},{}".format(time.ctime(int(start_time)), time.ctime(int(end_time)), 
                                                timestep, steps, nbodies, execution_time, comment)
    f=open('python_execution_history.csv','a')
    f.write("\n")
    f.write(omp_execution_history)
    f.close()