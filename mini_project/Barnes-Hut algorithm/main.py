from quadtree import quadtree, node, particle
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(100)

total_particles = 100
total_cores = 4
particles_per_core = total_particles / total_cores

core_total_particles = particles_per_core

t_steps = 10

# for t_i in range(t_steps):
#     pass
width, height = 20, 20

N_stars = 100
x0, y0 = 0, 0
x = np.vstack(np.random.uniform(-width*0.5, width*0.5, N_stars))
y = np.vstack(np.random.uniform(-height*0.5, height*0.5, N_stars))
mass = np.vstack(np.random.uniform(1, 10, N_stars))
coords = np.hstack((x, y, mass))

# print(coords)

boundary = node(*[x0, y0, width, height])
capacity = 1
qtree = quadtree(boundary, capacity, 0)

stars = []
for coord in coords:
    stars.append(particle(*coord))

for i, star in zip(range(N_stars), stars):
    qtree.insert(star)


# ax = plt.subplot()
# ax.set_xlim(width*-0.5, width*0.5)
# ax.set_ylim(height*-0.5, height*0.5)
# qtree.show(ax)
# ax.scatter([star.x for star in stars], [star.y for star in stars], s=8)
# plt.show()

# boundary = node(*[x0 + width*0.25, y0 + height*0.25, width*0.25, height*0.25])
# print(qtree.search(boundary))

# for boundary, data in qtree.search(boundary):
#     print(boundary, data)
