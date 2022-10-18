import numpy as np

class star:
    """
    Star object
    
    """
    def __init__(self, x, y, mass):
        star.x = x          # Star's y position, pc
        star.y = y          # Star's x position, pc
        star.mass = mass    # Star mass, M_sun

class boundary:
    """
    
    """

    def __init__(self) -> None:
        """
        
        """
        pass        

class quad_tree:
    """
    Quad tree implentation for Barnes-Hut algorithm
    """
    def __init__(self, boundary, max_capcity=4):
        """
        
        """
        self.boundary = boundary
        self.max_capcity = max_capcity
        self.points = []
    
    def subdivide(self):
        """
        
        """
        self.northwest = quad_tree()
        self.northeast = quad_tree()
        self.southwest = quad_tree()
        self.southeast = quad_tree()
