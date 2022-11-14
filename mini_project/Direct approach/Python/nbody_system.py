import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
    
    def draw(self, ax):

        ax.scatter(self.x, self.y, self.z, label=self.name)
        


class system:

    def __init__(self, nbody, steps):
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

    def run(self, timestep, steps, display=False):
        """
        
        
        """
        savepath = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python\figures"
        self.sframes = frames(steps+1)
        self.sframes.insert(self.bodies)

        for step in range(0, steps):
            self.update(timestep)
            if (display == True):
                fig = plt.figure()
                ax = plt.axes(projection = '3d')
                self.display(ax)
                save1 = "%s\%s.png" % (savepath, step)
                plt.savefig(save1)

        self.sframes.save()



    def display(self, ax):
        for body in self.bodies:
            body.draw(ax)



