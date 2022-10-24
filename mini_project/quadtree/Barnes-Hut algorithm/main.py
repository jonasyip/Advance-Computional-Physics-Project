from quadtree import quadtree, node, particle
import numpy as np

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
x = np.random.uniform(-width*0.5, width*0.5, N_stars)
y = np.random.uniform(-height*0.5, height*0.5, N_stars)
mass = np.random.uniform(1, 10, N_stars)
coords = np.column_stack((x,y))

boundary = node(*[0, 0, width, height])
capacity = 4
qtree = quadtree(boundary, capacity, 0)

stars = []
for coord in coords:
    stars.append(particle(*coord))

for i, star in zip(range(100), stars):
    # print(i)
    qtree.insert(star)
    print(qtree.stars)