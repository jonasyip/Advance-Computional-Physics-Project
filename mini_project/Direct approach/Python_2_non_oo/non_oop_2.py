import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def run(timestep, iterations):
    #Constants
    G_CONST = 6.67430E-2

    #Load initial system
    path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python_2_non_oo\initial_conditions.csv"
    initial_system = np.loadtxt(path, skiprows=2, delimiter=',', dtype=np.float64)
    initial_system = initial_system[0:10]
    # print(initial_system)
    global total_bodies
    total_bodies = len(initial_system)

    nbody_system = initial_system

    global nbody_system_w_time
    nbody_system_w_time = np.zeros(iterations+1, dtype=object)
    nbody_system_w_time[0] = initial_system

    for count_k in range(1, iterations):
        count_j = 0
        a_to_update = np.zeros(total_bodies, dtype=object)
        for body1 in nbody_system:
            count = 0
            a_array = np.zeros(((total_bodies-1), 3))  
            for body2 in nbody_system:
                if (body1[0] != body2[0]):
                    # print("\nbody1 %s , body2 %s" % (body1, body2))
                    r1 = np.array([body1[2], body1[3], body1[4]])
                    r2 = np.array([body2[2], body2[3], body2[4]])
                    r_diff = np.subtract(r1, r2)
                    # print("r1 %s \n r2 %s \n r_diff %s \n" % (r1, r2, r_diff))
                    a_i = -1*G_CONST*((body2[1]*r_diff) / np.power(np.absolute(r_diff), 3))
                    # print(a_i)
                    a_array[count] = a_i
                    count += 1
            acceleration = np.sum(a_array, axis=0)
            a_to_update[count_j] = acceleration
            count_j += 1

        # print("a_to_update ", a_to_update)
        # print("nbody_system \n", nbody_system)
        for body1, i, accel in zip(nbody_system, range(total_bodies), a_to_update):
            # print("body1, i, accel", body1, i, accel)
            #New velocity
            new_vx = body1[5] + accel[0]*timestep
            new_vy = body1[6] + accel[1]*timestep
            new_vz = body1[7] + accel[2]*timestep
            

            #body
            new_x = body1[2] + (new_vx * timestep)    #new_x = odd_x + (velocity + accel*time)*time
            new_y = body1[3] + (new_vy * timestep)
            new_z = body1[4] + (new_vz * timestep)

            #Update values
            nbody_system[i, 2] = new_x
            nbody_system[i, 3] = new_y
            nbody_system[i, 4] = new_z

            nbody_system[i, 5] = new_vx
            nbody_system[i, 6] = new_vy
            nbody_system[i, 7] = new_vz

        nbody_system_w_time[count_k] = nbody_system
        # print("count_k ", count_k)
        # print("\n nbody_system_w_time ", nbody_system_w_time)
        # print("\n \n \n")
        print("count_k ", count_k)
        print(nbody_system)
        print("\n \n")
        

timestep = 86400
iterations = 10
run(timestep, iterations)

# def animate(i):
#     ax.clear()
#     system_t = nbody_system_w_time[i]
#     # print(system_t)
#     # graph.set_array = (system_t[:, 2] , system_t[:, 3], system_t[:, 4])
#     ax.title('Time={} s'.format(i*timestep))
#     ax.set_data(system_t[:, 2] , system_t[:, 3], system_t[:, 4])



fig = plt.figure()
ax = fig.add_subplot(projection = '3d')
# ax.set_xlim((-5E25, 5E25))
# ax.set_ylim((-5E25, 5E25))
# ax.set_zlim((-5E25, 5E25))



plt.show()
print("\n nbody_system_w_time", nbody_system_w_time)
system_t = nbody_system_w_time[2]
print(system_t)
print(system_t[0])
print("\n")
print(system_t[0, 1])

savepath = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python_2_non_oo\run"
for system_t, i in zip(nbody_system_w_time, range(len(nbody_system_w_time))):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    title = ax.set_title('{}'.format(i*timestep))
    system_t = nbody_system_w_time[i]
    for part in system_t:
        ax.scatter(part[2] , part[3], part[4])
    save = "%s\%s.png" % (savepath, i)
    plt.savefig(save)
    plt.close()