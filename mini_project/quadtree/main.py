import matplotlib.pyplot as plt
import numpy as np
from quadtree_script import quadtree, square, star, node


def compute_com(mass, cm):
    """
    


    """
    a = 0

np.random.seed(100)

N_stars = 100
x = np.random.uniform(-10, 10, N_stars)
y = np.random.uniform(-10, 10, N_stars)
mass = np.random.uniform(1, 10, N_stars)
coords = np.column_stack((x,y))

treeStructure = {
    "Node" : None,
    "Level" : None,
    "quadrant" : None,
    "Data" : None

}

stars = []
for coord in coords:
    stars.append(star(*coord))

width = 20
height = 20
boundary = square(*[0, 0, width, height])
capacity = 4
qtree = quadtree(boundary, capacity, 0)
for i, star in zip(range(100), stars):
    # print(i)
    qtree.insert(star)
    print(qtree.stars)
#     print(qtree.stars)
# print(len(qtree.stars))
# print(node)



# ax = plt.subplot()

# ax.set_xlim(width*-0.5, width*0.5)
# ax.set_ylim(height*-0.5, height*0.5)
# qtree.show(ax)

# ax.scatter([star.x for star in stars], [star.y for star in stars], s=8)
# plt.show()



