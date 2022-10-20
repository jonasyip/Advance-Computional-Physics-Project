import numpy as np


class star:
    """
    Star 
    """
    def __init__(self, x, y, mass=None):
        self.x = x          # Star y position, pc
        self.y = y          # Star x position, pc
        self.mass = mass    # Star mass, M_sun

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.mass}]"
       
    
    def array(self):
        array = np.array(f"[{self.x}, {self.y}, {self.mass}]")
        return array


    
    # def __str__(self):
    #     return f"star(x={self.x}, y={self.y}, mass={self.mass})"


class square:

    """
    Boundary rectangle object

    Boundary constrains the system

    """

    def __init__(self, centre_x, centre_y, width, height): #
        """

        
        """
        #Boundary cube
        self.centre_x = centre_x #
        self.centre_y = centre_y
        self.width = width
        self.height = height


    def __repr__(self):
        return f"[{self.centre_x}, {self.centre_y}, {self.width}, {self.height}]"
        

    def contains(self, star): #
        """
        Checks if the star is within the cube boundary.
         (cx - width)  <= x < (cx + width)
         (cy - height) <= y < (cy + width)

        Parameters
        ----------
        star : object

        Returns
        -------
        within_boundary : boolean

        """
        star_x = star.x
        star_y = star.y

        
        if (star_x >= (self.centre_x - (self.width*0.5)) and
            star_x < (self.centre_x + (self.width*0.5)) and
            star_y >= (self.centre_y - (self.height*0.5)) and
            star_y < (self.centre_y + (self.height*0.5))): 
            within_boundary = True
        else:
            within_boundary = False
        
        return within_boundary
                  

    def show(self, ax, c='k', lw=1, **kwargs):
        x1 = self.centre_x - (self.width*0.5)
        x2 = self.centre_x + (self.width*0.5)
        y1 = self.centre_y - (self.height*0.5)
        y2 = self.centre_y + (self.height*0.5)
        ax.plot([x1,x2,x2,x1,x1], [y1,y1,y2,y2,y1], c=c, lw=lw, **kwargs)





    
    
class quadtree:
    """
    Quadtree implentation for Barnes-Hut algorithm
    """
    def __init__(self, boundary, max_capcity=4):
        """
        
        """
        self.max_capcity = max_capcity #Maximum children
        self.boundary = boundary
        self.divided = False
        # self.depth = depth
        self.stars = [] #List of star objects
    
    def __repr__(self):
        return f"[{self.boundary}, {self.max_capcity}]"
    
    def __str__(self):
        return f"quadtree(boundary={self.boundary}, max_capcity={self.max_capcity})"

        
    
    def subdivide(self):
        """
        Sub division creates eight new cubes in the root or in existing cube
        
        """
        #Initialise boundary as local variables
        centre_x = self.boundary.centre_x        #Boundary x centre (pc)
        centre_y = self.boundary.centre_y        #Boundary y centre (pc)

        width = self.boundary.width              #Boundary width (pc)
        height = self.boundary.height            #Boundary height (pc)


        #Four quadrants
        # Subdividing -> *0.25

        #Quadrants
        #north-west boundary
        nw_boundary = square(
            centre_x - (width * 0.25),
            centre_y + (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.nw = quadtree(nw_boundary, self.max_capcity)
        
        #north-east boundary
        ne_boundary = square(
            centre_x + (width * 0.25),
            centre_y + (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.ne = quadtree(ne_boundary, self.max_capcity)

        #south-west boundary
        sw_boundary = square(
            centre_x - (width * 0.25),
            centre_y - (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.sw = quadtree(sw_boundary, self.max_capcity)

        #south-east boundary
        se_boundary = square(
            centre_x + (width * 0.25),
            centre_y - (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.se = quadtree(se_boundary, self.max_capcity)

        self.divided = True

    def insert(self, star):
        """
        Case 1: If not within boundary -> Pass
        Case 2: If one star -> Store as leaf node
        Case 3: If more than one star -> Store as twig node
        Case 4: If no star -> Pass
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
            self.nw.insert(star) or
            self.ne.insert(star) or
            self.sw.insert(star) or
            self.se.insert(star))
        
    def show(self, ax):
        # square(self.boundary.centre_x, self.boundary.centre_y, self.boundary.width, self.boundary.height)
        self.boundary.show(ax)
        if (self.divided == True):
            self.nw.show(ax)
            self.ne.show(ax)
            self.sw.show(ax)
            self.se.show(ax)



def setup():
    """
    
    """
    boundary = square(0)
    octTree = quadtree(boundary, 8)

