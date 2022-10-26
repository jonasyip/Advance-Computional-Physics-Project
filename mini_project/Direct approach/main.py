from solar_system import solarsystem, body
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


file_name = r"C:\\Users\\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\system.csv"
df = pd.read_csv(file_name, header=1)
solar_system = np.array(df)

nbody = len(solar_system)
ssystem = solarsystem(nbody) 

for name, mass, radius, x, y, z, vx, vy, vz in solar_system:
    body_data = body(name, mass, radius, x, y, z, vx, vy, vz)
    ssystem.insert(body_data)

# for bodyy in ssystem.bodies:
#     print(bodyy.name)
#     print(bodyy.mass)



ax = plt.subplot()
ssystem.display(ax)
plt.title("0")
ax.legend()
plt.show()

ssystem.update(86400)
ax = plt.subplot()
ssystem.display(ax)
plt.title("1")
plt.show()
