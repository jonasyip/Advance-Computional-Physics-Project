# import numpy as np


class star:
    """
    Star object containing the star's (x, y, z) coordinate and mass
    
    """
    def __init__(self, x, y, z, mass=None):
        self.x = x          # Star y position, pc
        self.y = y          # Star x position, pc
        self.z = z         # Star z position, pc
        self.mass = mass    # Star mass, M_sun

    def __repr__(self):
        # rep = 'star(x={}, y={}, z={}, mass={})'.format(self.x, self.y, self.z, self.mass)
        rep = f"star(x={self.x}, y={self.y}, z={self.z}, mass={self.mass})"
        return rep
    
    def __str__(self):
        return f"star(x={self.x}, y={self.y}, z={self.z}, mass={self.mass})"


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
        self.centre_x = centre_x #
        self.centre_y = centre_y
        self.centre_z = centre_z
        self.width = width
        self.height = height
        self.length = length

#     def __repr__(self):
        # return '{}: {}'.format(str(self.x, self.y)). repr(self.mass)
        

    def contains(self, star): #
        """
        Checks if the star is within the cube boundary.
         (cx - width)  <= x < (cx + width)
         (cy - height) <= y < (cy + width)
         (cz - length) <= z < (cz + length)

        Parameters
        ----------
        star : object

        Returns
        -------
        within_boundary : boolean

        """
        star_x = star.x
        star_y = star.y
        star_z = star.z
        
        if (star_x > (self.centre_x - self.width) and
            star_x < (self.centre_x + self.width) and
            star_y > (self.centre_y - self.height) and
            star_y < (self.centre_y + self.height) and
            star_z > (self.centre_z - self.length) and
            star_z < (self.centre_z + self.length)): 
            within_boundary = True
        else:
            within_boundary = False
        
        return within_boundary
                  

#     def draw()
    
    
class octree:
    """
    Octree implentation for Barnes-Hut algorithm
    """
    def __init__(self, boundary, max_capcity=8):
        """
        
        """
        self.max_capcity = max_capcity #Maximum children
        self.boundary = boundary
        self.divided = False
        # self.depth = depth
        self.stars = [] #List of star objects

        
    
    def subdivide(self):
        """
        Sub division creates eight new cubes in the root or in existing cube
        
        """
        #Initialise boundary as local variables
        centre_x = self.boundary.centre_x        #Boundary x centre (pc)
        centre_y = self.boundary.centre_y        #Boundary y centre (pc)
        centre_z = self.boundary.centre_z        #Boundary z centre (pc)
        width = self.boundary.width              #Boundary width (pc)
        height = self.boundary.height            #Boundary height (pc)
        length = self.boundary.length            #Boundary length (pc)

        #Birds eye view of a cube (Looking down on a cube)
        # You see four quadrants on two layers.
        # Layer 1: top, layer 2: bottom

        #----------TOP----------
        #Top north-west boundary
        top_nw_boundary = cube(
            centre_x - (width * 0.5),
            centre_y + (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)
        self.top_nw = octree(top_nw_boundary, self.max_capcity)
        
        #Top north-east boundary
        top_ne_boundary = cube(
            centre_x + (width * 0.5),
            centre_y + (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)
        self.top_ne = octree(top_ne_boundary, self.max_capcity)

        #Top south-west boundary
        top_sw_boundary = cube(
            centre_x - (width * 0.5),
            centre_y - (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)
        self.top_sw = octree(top_sw_boundary, self.max_capcity)

        #Top south-east boundary
        top_se_boundary = cube(
            centre_x + (width * 0.5),
            centre_y - (height * 0.5),
            centre_z + (length * 0.5),
            width,
            height,
            length)
        self.top_se = octree(top_se_boundary, self.max_capcity)

        #----------BOTTOM----------
        #Bottom north-west boundary
        bottom_nw_boundary = cube(
            centre_x - (width * 0.5),
            centre_y + (height * 0.5),
            centre_z - (length * 0.5),
            width,
            height,
            length)
        self.bottom_nw = octree(bottom_nw_boundary, self.max_capcity)
        
        #Bottom north-east boundary
        bottom_ne_boundary = cube(
            centre_x + (width * 0.5),
            centre_y + (height * 0.5),
            centre_z - (length * 0.5),
            width,
            height,
            length)
        self.bottom_ne = octree(bottom_ne_boundary, self.max_capcity)
        
        #Bottom south-west boundary
        bottom_sw_boundary = cube(
            centre_x - (width * 0.5),
            centre_y - (height * 0.5),
            centre_z - (length * 0.5),
            width,
            height,
            length)
        self.bottom_sw = octree(bottom_sw_boundary, self.max_capcity)
        
        #Bottom south-east boundary
        bottom_se_boundary = cube(
            centre_x + (width * 0.5),
            centre_y - (height * 0.5),
            centre_z - (length * 0.5),
            width,
            height,
            length)
        self.bottom_se = octree(bottom_se_boundary, self.max_capcity)
            
        self.divided = True

    def insert(self, star):
        """
        Case 1: If no star ->
        Case 2: If one star -> Store as leaf node
        Case 3: If more than one star -> Store as twig node

        """
        #Case 1
        if (self.boundary.contains(star) == False): #If star is not contained within boundary
            return False

        #Case 2
        if (len(self.stars) < self.max_capcity): #If cube is below capacity
            self.stars.append(star) #Leaf node
            return True
        
        #Case 3
        else:
            if (self.divided == False): 
                self.subdivide()

            #Return
            return(
            self.top_nw.insert(star) or
            self.top_ne.insert(star) or
            self.top_sw.insert(star) or
            self.top_se.insert(star) or

            self.bottom_nw.insert(star) or
            self.bottom_ne.insert(star) or
            self.bottom_sw.insert(star) or
            self.bottom_se.insert(star))


def setup():
    """
    
    """
    boundary = cube(0)
    octTree = octree(boundary, 8)

