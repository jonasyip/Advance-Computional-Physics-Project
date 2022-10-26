import numpy as np

a = [1, 2, 3]
b = [4, 5, 6]
dst = np.linalg.norm(np.subtract(a, b))

np.random.seed(100)       #Seed set for reproducibility

def distance_between(coord_1, coord_2):
    """
    Calculates the Euclidean distance between two points of arbitary units.

    Parameters
    ----------
    coord_1 : array_like
        Point 1, in a list [x1, y1, z1].

    coord_2 : array_like
        Point 2, in a list [x2, y2, z2]

    Returns
    -------
    distance : float
        Euclidean distance between point 1 and point 2 in arbitary units.
    
    """
    # x_1, y_1, y_1 = coord_1
    # x_2, y_2, y_2 = coord_2

    distance = np.linalg.norm(np.subtract(coord_1, coord_2))

    return distance


