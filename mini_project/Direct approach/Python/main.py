import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from nbody_system import system, body
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')



file_name = r"mini_project\Direct approach\Python\system.csv"
df = pd.read_csv(file_name, header=1)
solar_system = np.array(df)

nbody = len(solar_system)
ssystem = system(nbody) 

for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
    body_data = body(name, mass, x, y, z, vx, vy, vz)
    ssystem.insert(body_data)

ssystem.run(20000, 10, True)

# steps = 10
# positions = np.zeros(steps, dtype=object)


# for i, dt in zip(range(steps), range(0, steps*86400, 86400)):
#     ssystem.update(dt)
#     t_pos = np.zeros(nbody, dtype=object)
#     for j, planet in zip(range(nbody), ssystem.bodies):
#         t_pos[j] = planet.position()
#     positions[i] = t_pos
    

# print(positions[2])



#---------
# fig = plt.figure()
# ax = plt.axes(projection = '3d')

# def Animate3D(k):
#     for i, ligne in enumerate(lignes, 0):
#         ligne.set_data(Y[k:max(1, k - trail[0]):-1, 3*i], Y[k:max(1, k - trail[0]):-1, 3*i + 1])
#         ligne.set_3d_properties(Y[k:max(1, k - trail[0]):-1, 2])

#     return lignes


# lignes = [ax.plot([], [], "o-", markevery = 10000)[0] for _ in range(N)]

# anim3D = animation.FuncAnimation(fig, Animate3D, frames = n, interval = 30, blit = False)

# plt.show()


