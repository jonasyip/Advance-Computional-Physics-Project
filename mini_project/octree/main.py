from scripts import star, cube, octree
import numpy as np

#taskID

np.random.seed(100)

N_stars = 10

height = 100
width = 100
length = 100
mass_range = [2, 10]
# coords = random.random(N_stars) * height
# coords = 0 + 0.5 * np.random.randn(N_stars, 3) * height 


coords = [[1, 2, 3],
          [-4, -5, -6],
          [7, -8, 9]]

print(coords)
# stars = [star(*coord) for coord in coords]
stars = []
for coord in coords:
    print(star(*coord))
    stars.append(star(*coord))
print(stars)    

root = cube(width*0.5, height*0.5, length*0.5, width, height, length)

otree = octree(root, 8)

# for star in stars:
#     # print(star)

# for star in stars:
#     otree.insert(star)

# print(otree)