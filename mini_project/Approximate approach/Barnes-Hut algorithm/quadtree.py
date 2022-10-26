
class particle:
    """
    Star 
    """
    def __init__(self, x, y, mass=None):
        self.x = x          # Star y position, pc
        self.y = y          # Star x position, pc
        self.mass = mass    # Star mass, M_sun

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.mass}]"
    
    def __str__(self):
        return f"particle({self.x}, {self.y}, {self.mass})"

class node:

    mass = None
    cm = None
    children = None

    def __init__(self, centre_x, centre_y, width, height): #
        """

        
        """
        #key
        

        #Boundary cube
        self.centre_x = centre_x #
        self.centre_y = centre_y
        self.width = width
        self.height = height

        #Centre of Mass (cm)

        
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
    def __init__(self, boundary, max_capcity=4, level=0):
        """
        
        """
        self.max_capcity = max_capcity #Maximum children
        self.boundary = boundary
        self.divided = False
        self.level = level
        self.stars = [] #List of star objects

    def __repr__(self):
        return f"[{self.boundary}, {self.max_capcity}, {self.level}]"
    
    def __str__(self):
        return f"quadtree(boundary={self.boundary}, max_capcity={self.max_capcity}, level={self.level})"


    def insert(self, star):
        """
        Case 1: If not within boundary -> Pass
        Case 2: If one star -> Store as leaf node
        Case 3: If more than one star -> Store as twig node
        Case 4: If no star -> Pass

        Recursive
        """


        #Case 1
        if (self.boundary.contains(star) == False): #If star is not contained within boundary
            return False

        #Case 2
        if (len(self.stars) < self.max_capcity): #If cube is below capacity
            self.stars.append(star) #Leaf node
            # node(self.boundary, star)
            return True
        
        #Case 3
        else:
            if (self.divided == False): 
                self.subdivide()

            
            if (self.nw.insert(star) == True):
                node.insert(self.nw.boundary, star)
                return True
            elif (self.ne.insert(star) == True):
                return True
            elif (self.sw.insert(star) == True):
                return True
            elif (self.se.insert(star) == True):
                return True
            else:
                return False
            
    def subdivide(self):
        """
        Sub division creates eight new cubes in the root or in existing cube
        
        """
        #Initialise boundary as local variables
        centre_x = self.boundary.centre_x        #Boundary x centre (pc)
        centre_y = self.boundary.centre_y        #Boundary y centre (pc)

        width = self.boundary.width              #Boundary width (pc)
        height = self.boundary.height            #Boundary height (pc)


        #Children
        # Four quadrants
        # Subdividing -> *0.25

        #Quadrants
        #north-west boundary
        nw_boundary = node(
            centre_x - (width * 0.25),
            centre_y + (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.nw = quadtree(nw_boundary, self.max_capcity, (self.level+1))
        
        #north-east boundary
        ne_boundary = node(
            centre_x + (width * 0.25),
            centre_y + (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.ne = quadtree(ne_boundary, self.max_capcity, (self.level+1))

        #south-west boundary
        sw_boundary = node(
            centre_x - (width * 0.25),
            centre_y - (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.sw = quadtree(sw_boundary, self.max_capcity, (self.level+1))

        #south-east boundary
        se_boundary = node(
            centre_x + (width * 0.25),
            centre_y - (height * 0.25),
            (width * 0.5),
            (height * 0.5))
        self.se = quadtree(se_boundary, self.max_capcity, (self.level+1))

        self.divided = True
        
    def show(self, ax):
        """
        
        """
        # square(self.boundary.centre_x, self.boundary.centre_y, self.boundary.width, self.boundary.height)
        self.boundary.show(ax)
        if (self.divided == True):
            self.nw.show(ax)
            self.ne.show(ax)
            self.sw.show(ax)
            self.se.show(ax)

    def search(self, boundary, stars_searched=None):
        """
        
        """
        if stars_searched is None:
            stars_searched = []

        for star in self.stars:
            if boundary.contains(star):
                data = [boundary, star]
                stars_searched.append(data)

        if (self.divided == True): #Recusive
            self.nw.search(boundary, stars_searched)
            self.ne.search(boundary, stars_searched)
            self.se.search(boundary, stars_searched)
            self.sw.search(boundary, stars_searched)
        return stars_searched
