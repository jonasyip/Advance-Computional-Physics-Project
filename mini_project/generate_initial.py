import numpy as np
import matplotlib.pyplot as plt
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

N_size = 100

x = random.random(N_size) #0 to 1

theta = np.arccos(1 - 2*x) #Arccos is used to distribute theta

phi = random.uniform(0, 2 * np.pi, N_size) #Phi in range of [0, 2*pi] for distrubtion

x_list = (r * np.sin(theta) * np.cos(phi)) 
y_list = (r * np.sin(theta) * np.sin(phi))
z_list = (r * np.cos(theta))
mass_list = random.gamma(6, 1, N_size)

print(x_list)
# count, bins, ignored = plt.hist(mass_list, 50, density = True)
# plt.show()

data = {
    "x_position (pc)" : x_list,
    "y_position (pc)" : y_list,
    "z_position (pc)" : z_list,
    "Mass (kg)" : mass_list 
}


# fig = plt.figure(figsize=(6, 6))
# plt.scatter(x_list, z_list)
# plt.show()

filename = "initial_conditions.csv"
df = pd.DataFrame(data)
df.to_csv('filename')

print("%s created" % (filename))