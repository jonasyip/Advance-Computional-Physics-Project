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
    Boundary rectangle

    """

    def __init__(self, centre_x, centre_y, width, height):
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
        #NORTH WEST
        northWest_boundary = boundary(
                self.centre_x + (self.width * 0.5),
                self.centre_y + (self.height * 0.5),
                (self.width * 0.5),
                (self.height * 0.5))
        self.northWest = quad_tree(northWest_boundary)
        
        #NORTH EAST
        northEast_boundary = boundary(
                self.centre_x + (self.width * 0.5),
                self.centre_y + (self.height * 0.5),
                (self.width * 0.5),
                (self.height * 0.5))
        self.northEast = quad_tree(northEast_boundary)

        #SOUTH WEST
        southWest_boundary = boundary(
                self.centre_x + (self.width * 0.5),
                self.centre_y + (self.height * 0.5),
                (self.width * 0.5),
                (self.height * 0.5))
        self.southwest = quad_tree()
        
        #SOUTH EAST
        southEast_boundary = boundary(
                self.centre_x + (self.width * 0.5),
                self.centre_y + (self.height * 0.5),
                (self.width * 0.5),
                (self.height * 0.5))
        self.southEast = quad_tree(southEast_boundary)
