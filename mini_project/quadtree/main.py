import matplotlib.pyplot as plt
import numpy as np
from quadtree_scripts import quadtree, square, star

np.random.seed(100)

N_stars = 100
x = np.random.uniform(-100, 100, N_stars)
y = np.random.uniform(-100, 100, N_stars)
coords = np.column_stack((x,y))
# print(coords)

stars = []
for coord in coords:
    stars.append(star(*coord))

width = 200
height = 200
boundary = square(*[0, 0, width, height])
qtree = quadtree(boundary, 1)
for star in stars:
    qtree.insert(star)

ax = plt.subplot()
ax.set_xlim(width*-0.5, width*0.5)
ax.set_ylim(height*-0.5, height*0.5)
qtree.show(ax)

ax.scatter([star.x for star in stars], [star.y for star in stars], s=8)
plt.show()


