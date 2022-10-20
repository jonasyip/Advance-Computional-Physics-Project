import numpy as np
from scripts import quadtree, square, star


coords = [[1, 2, 3], [3, 4, 5], [5, 6, 7]]

stars = []
for coord in coords:
    stars.append(star(*coord))

print(stars[0].x)

