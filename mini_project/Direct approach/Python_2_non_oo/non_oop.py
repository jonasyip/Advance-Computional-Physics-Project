import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation



def run(timestep, iterations):
    #Constants
    G_CONST = 6.67430E-11

    #Load initial system
    path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python_2_non_oo\system.csv"
    initial_system = np.loadtxt(path, skiprows=2, delimiter=',', dtype=np.float64)
    global total_bodies
    total_bodies = len(initial_system)

    nbody_system = initial_system

    global nbody_system_w_time
    nbody_system_w_time = np.zeros(iterations+1, dtype=object)
    nbody_system_w_time[0] = initial_system

    for count_k in range(iterations):
        a_to_update = np.zeros(total_bodies, dtype=object)

        for body1, count_j in zip(nbody_system, range(total_bodies)):
            # a_array = np.zeros(((total_bodies-1), 3))     #Body 1 acceleration array (m/s)
            a_array = np.zeros((total_bodies-1), dtype=object)
            # print(a_array)
            count_i = 0
            for body2 in nbody_system:
                if (body1[0] != body2[0]): #Body1 calculates other than itself
                    print(body1, body2)
                    # x1 = 
                    r_diff = np.array([(body1[2]-body2[2]),   #x1 - x2
                                      (body1[3]-body2[3]),    #y1 - y2
                                      (body1[4]-body2[4])])   #z1 - z2
                    print("r_diff ", r_diff)
                    a_i = -1*G_CONST*((body2[1]*r_diff) / np.power(np.absolute(r_diff), 3))
                    # print(a_i)
                    #where_are_NaNs = isnan(a)
                    # a[where_are_NaNs] = 0
                    a_array[count_i] = a_i
                    count_i += 1
                    print("a_i ", a_i)
            
            # print("a_array ", a_array)
            acceleration = np.sum(a_array, axis=0)
            # print("acceleration ", acceleration)
            a_to_update[count_j] = acceleration
            count_j += 1

        # print("a_to_update ", a_to_update)

        for i, accel in zip(range(total_bodies), a_to_update):
            new_x = body1[2] + (body1[5] + accel[0]*timestep) * timestep    #new_x = odd_x + (velocity + accel*time)*time
            new_y = body1[3] + (body1[6] + accel[1]*timestep) * timestep
            new_z = body1[4] + (body1[7] + accel[2]*timestep) * timestep
 
            nbody_system[i, 2] = new_x
            nbody_system[i, 3] = new_y
            nbody_system[i, 4] = new_z

        nbody_system_w_time[count_k+1] = nbody_system
        
    

    #name, mass, x, y, z, vx, vy, vz
    #   0,    1, 2, 3, 4,  5,  6,  7

timestep = 10000
run(timestep, 3)

print(nbody_system_w_time)

# def animate(i):
#     system_t = nbody_system_w_time[i]
#     graph._offsets3d = (system_t[:, 2] , system_t[:, 3], system_t[:, 4])
#     title.set_text('Time={} s'.format(i*timestep))


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# title = ax.set_title('3D Test')
# ax.set_xlim((-5E9, 5E9))
# ax.set_ylim((-5E9, 5E9))
# ax.set_zlim((-5E9, 5E9))

# system_t = nbody_system_w_time[0]
# graph = ax.scatter(system_t[:, 2] , system_t[:, 3], system_t[:, 4])

# ani = animation.FuncAnimation(fig, animate, 
#                                interval=200, blit=False)

# plt.show()