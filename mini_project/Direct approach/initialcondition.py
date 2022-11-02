import matplotlib.pyplot as plt
import numpy as np
import numpy.random as random
import pandas as pd

np.random.seed(100)       #Seed set for reproducibility


#x_position, y_position, z_position, Mass
#1 pc = 3.0856E16 (30856775814913670) meters
#4.30091E-3 pc (M_Sun)^{-1} (km/s)^{2}

r = 15 #pc
x = []
y = []
z = []

N_size = 100000

x = random.random(N_size) #0 to 1

theta = np.arccos(1 - 2*x) #Arccos is used to distribute theta

phi = random.uniform(0, 2 * np.pi, N_size) #Phi in range of [0, 2*pi] for distrubtion

r = 1E8
x_list = (r * np.sin(theta) * np.cos(phi)) 
y_list = (r * np.sin(theta) * np.sin(phi))
z_list = (r * np.cos(theta))
mass_list = np.full(N_size, 6000)
vx_list = np.zeros(N_size)
vy_list = np.zeros(N_size)
vz_list = np.zeros(N_size)


data = {
    "Mass" : mass_list,
    "x" : x_list,
    "y" : y_list,
    "z" : z_list,
    "vx" : vx_list,
    "vy" : vy_list,
    "vz" : vz_list
}

# fig = plt.figure(figsize=(6, 6))
# plt.scatter(x_list, z_list)
# plt.show()

filename = "initial_conditions.csv"
df = pd.DataFrame(data)
df.to_csv(filename)

print("%s created" % (filename))