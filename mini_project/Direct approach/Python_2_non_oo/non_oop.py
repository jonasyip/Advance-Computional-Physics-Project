import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation



def run(timestep, iterations):
    #Constants
    G_CONST = 6.67430E-11

    #Load initial system
    path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python_2_non_oo\system.csv"
    initial_system = np.loadtxt(path, skiprows=2, delimiter=',', dtype=np.float64)
    print(initial_system)
    global total_bodies
    total_bodies = len(initial_system)
    

    #name, mass, x, y, z, vx, vy, vz
    #   0,    1, 2, 3, 4,  5,  6,  7

timestep = 100000
run(timestep, 100)

print(nbody_system_w_time)

def animate(i):
    system_t = nbody_system_w_time[i]
    graph._offsets3d = (system_t[:, 2] , system_t[:, 3], system_t[:, 4])
    title.set_text('Time={} s'.format(i*timestep))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
title = ax.set_title('3D Test')
ax.set_xlim((-5E10, 5E9))
ax.set_ylim((-5E10, 5E9))
ax.set_zlim((-5E10, 5E9))

system_t = nbody_system_w_time[0]
graph = ax.scatter(system_t[:, 2] , system_t[:, 3], system_t[:, 4])

ani = animation.FuncAnimation(fig, animate, 
                               interval=200, blit=False)

plt.show()