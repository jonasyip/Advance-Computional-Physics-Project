# import numpy as np

from calendar import c


class star:
    """
    Star object containing the star's (x, y, z) coordinate and mass
    
    """
    def __init__(self, x, y, z, mass):
        star.x = x          # Star y position, pc
        star.y = y          # Star x position, pc
        star.z = z         # Star z position, pc
        star.mass = mass    # Star mass, M_sun

class cube:
    #Rename as cube?
    """
    Boundary rectangle object

    Boundary constrains the system

    """

    def __init__(self, centre_x, centre_y, centre_z, width, height, length): #
        #Add centre_z in the arguments
        """

        
        """
        #Boundary cube
        self.x = centre_x #
        self.y = centre_y
        self.z = centre_z
        self.width = width
        self.height = height
        self.lenght = length

#     def __repr__(self):
        # return '{}: {}'.format(str(self.x, self.y)). repr(self.mass)
        

    def contains(star): #
        """
        Checks if the star is within the boundary. 


        Parameters
        ----------
        star : object
                


        Returns
        -------
        within_boundary : boolean

        """
        #Contains need to be made in 3D
        if (star.x > self.centre_x - self.width 
            and star.x < self.centre_x + self.width
            and star.y > self.centre_y - self.height
            and star.y < self.centre_y + self.height): 
            within_boundary = True
        else:
            within_boundary = False
        
        return within_boundary
                  

class oct_tree:
    """
    Quad tree implentation for Barnes-Hut algorithm
    """
    def __init__(self, boundary, max_capcity=8):
        """
        
        """
        self.max_capcity = max_capcity #Maximum children
        self.boundary = boundary
        self.divided = False
        self.stars = [] #List of star objects

        
    
    def subdivide(self):
        """
        Sub division creates eight new cubes in the root or in a cube
        
        """
        #Initialise boundary as local variables
        centre_x = self.centre_x        #Boundary x centre (pc)
        centre_y = self.centre_y        #Boundary y centre (pc)
        centre_z = self.centre_z        #Boundary z centre (pc)
        width = self.width              #Boundary width (pc)
        height = self.height            #Boundary height (pc)
        length = self.length            #Boundary lenght (pc)

        #Note to self - 3D

        #Birds eye view of a cube (Looking down on a cube)
        # You see four quadrants on two layers, top and bottom

        #TOP
        #Top north-west boundary
        top_nw_boundary = cube(
            centre_x - (width * 0.5),
            centre_y + (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)
        
        #Top north-east boundary
        top_ne_boundary = cube(
            centre_x + (width * 0.5),
            centre_y + (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)
        
        #Top south-west boundary
        top_sw_boundary = cube(
            centre_x - (width * 0.5),
            centre_y - (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)
        
        #Top south-east boundary
        top_se_boundary = cube(
            centre_x + (width * 0.5),
            centre_y - (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)


        #BOTTOM
        #Bottom north-west boundary
        

        self.divided = True

    def insert(self, star):
        """
        
        If one star -> Store as leaf node
        If more than one star -> Store as twig node

        """
        if (self.boundary.contains(star) == False): #If star is not contained
            return 0

        if (len(self.stars) < self.max_capcity): #If quad is below capacity
            self.stars.append(star) #Leaf node
        else:
            if (self.divided == False): 
                self.subdivide()
                self.divided = True

            #Return
            self.northWest.insert(star)
            self.northEast.insert(star)
            self.southWest.insert(star)
            self.southEast.insert(star)


def setup():
    """
    
    """
    boundary = cube(0)
    octTree = oct_tree(boundary, 8)

    for i in range(8):
        s = Point()