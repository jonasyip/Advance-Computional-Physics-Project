import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpi4py import MPI
import time
import sys

comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()

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
            data = np.array([star.id, star.mass, star.x, star.y, star.z, star.vx, star.vy, star.vz])
            star_data[i] = data

        self.system_frames[self.frame_count] = star_data
        self.frame_count += 1
    
    def save(self):
        """
        Saves all the system frames as a .npy
        """
        path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python"
        savename = "frames_mpi.npy"
        savepath = "%s\%s" % (path, savename)
        np.save(savename, self.system_frames)


class body:
    def __init__(self, id, mass, x, y, z, vx, vy, vz):

        self.id = id                #Name of the body
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

        self.masses = np.zeros(nbody, dtype=object)

        


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
            self.masses[self.bodycount] = body.mass
            self.bodycount += 1
        else:
            print("System reached maxmimum, body not added")

    def change_body(self, body_id, body1):
        self.bodies[body_id] = body1




    def update(self, timestep):
        """
        Updates the nbody system by t timestep

        Parameters
        ----------
        timestep : float
    
        """
        G_CONST = 6.67430E-11
        a_to_update = np.zeros(self.nbody, dtype=object)
        
        #MPI Allgather?
        #print("self.lower_body_id ", self.lower_body_id)
        #print("self.upper_body_id ", self.upper_body_id)

        nbody_per_rank = self.nbody / (size - 1) # -1 because of master rank
        lower_body_id = round(nbody_per_rank * (rank - 1))
        upper_body_id = round(rank * nbody_per_rank)

        print("\nrank ", rank)
        print("self.nbody ", self.nbody)
        print("self.bodycount ", self.bodycount)
        print("size ", size)
        print("self.nbody_per_rank ", nbody_per_rank)
        print("self.lower_body_id ", lower_body_id)
        print("self.upper_body_id ", upper_body_id)
        print("\n")

        for body_id in range(lower_body_id, upper_body_id):
            #print("body_id ", body_id)
            body1 = self.bodies[body_id]

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
            a_to_update[body1.id] = acceleration

        count = 0
        
        self.rank_bodies = np.zeros((upper_body_id - lower_body_id), dtype=object)
        for body_id in range(lower_body_id, upper_body_id):
            accel = a_to_update[body_id]
            body1 = self.bodies[body_id]
            body1.update(timestep, accel)
            
            self.rank_bodies[count] = body1
            count += 1
        # for body1, accel in zip(self.bodies, a_to_update): #remove
        #     body1.update(timestep, accel) #remove

        #self.sframes.insert(self.bodies) remove

    def this_rank_bodies(self):
        
        return self.rank_bodies




def main(timestep, steps, nbodies, comment=None):

    MASTER_RANK = 0

    if ((size-1) > nbodies):
        comm.Abort()
        print("Cannot to distribute workers")

    if comment is None:
        comment = ""

    
    if (rank == MASTER_RANK): 
        initial = np.loadtxt("initial_conditions.csv", skiprows=1, delimiter=',', dtype=np.float64)
        initial = initial[0:nbodies]
        nbody = int(len(initial))
        master_nbody_system = n_system(nbody)

        for id, mass, x, y, z, vx, vy, vz in initial:
            body_data = body(int(id), mass, x, y, z, vx, vy, vz)
            master_nbody_system.insert(body_data)

        sframes = frames(steps+1)
        sframes.insert(master_nbody_system.bodies) #Initial frame


    #Tag
    # 11 -
    # 21 - 

    print("rank ", rank)

    for step in range(0, steps):
        #print("rank %s step %s " % (rank, step))

        if (rank == MASTER_RANK):
            for worker_dest in range(1, size):
                print("worker_dest ", worker_dest)
                comm.send(master_nbody_system, dest=worker_dest, tag=11)

        else: #Worker
            
            nbody_system = comm.recv(source=MASTER_RANK, tag=11)
            #print("worker nbody_system", len(nbody_system.bodies))
            nbody_system.update(timestep)

            rank_nbodies = nbody_system.this_rank_bodies()
            #print("rank_nbodies ", len(rank_nbodies))
            comm.send(rank_nbodies, dest=MASTER_RANK, tag=21)


        if (rank == MASTER_RANK): #Insert frame
            for worker_source in range(1, size):
                recev_nbody_system = comm.recv(source=worker_source, tag=21)
                for body1 in recev_nbody_system:
                    #print(rank, body1.id)
                    master_nbody_system.change_body(body1.id, body1)
            
            sframes.insert(master_nbody_system.bodies)

    if (rank == MASTER_RANK): #Save frame
        sframes.save()
        print("Done")



      

    # else:
    #     for i in range(0, steps):
    


    #end 
    #sframes.save()


    

    # print("\nnbody_system_mpi.py")
    # print("==========================")
    # start_time = time.time()
    # nbody_system.run(timestep, steps)
    # end_time = time.time()
    # execution_time = (end_time - start_time)
    # print("Start {}".format(time.ctime(int(start_time))))
    # print("End   {}".format(time.ctime(int(end_time))))
    # print("Timestep: {} s \nSteps: {} \n{} bodies \nComment: {}".format(timestep, steps, nbodies,comment))
    # print("Execution time: {:.4f} s".format(execution_time))

    # #start_time,end_time,timestep,steps,bodies,threads,execution_time
    # omp_execution_history = "{},{},{},{},{},{},{}".format(time.ctime(int(start_time)), time.ctime(int(end_time)), 
    #                                             timestep, steps, nbodies, execution_time, comment)
    # f=open('python_mpi_execution_history.csv','a')
    # f.write("\n")
    # f.write(omp_execution_history)
    # f.close()

if int(len(sys.argv)) == 4: #Without comments
    main(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
elif int(len(sys.argv)) == 5: #With comments
    main(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), str(sys.argv[4]))
else:
    print("Usage: python {} <TIMESTEP> <ITERATIONS> <NBODIES> <(COMMENTS)>".format(sys.argv[0]))
