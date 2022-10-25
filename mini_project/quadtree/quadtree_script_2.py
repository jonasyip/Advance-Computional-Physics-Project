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


class node:

    def __init__(self, cx, cy, width, height):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height

        
        self.children = []
        self.stars = None
        n_stars = 0

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

        
        if (star_x >= (self.cx - (self.width*0.5)) and
            star_x < (self.cy + (self.width*0.5)) and
            star_y >= (self.cx - (self.height*0.5)) and
            star_y < (self.cy + (self.height*0.5))): 
            within_boundary = True
        else:
            within_boundary = False
        
        return within_boundary

    def createChildren(self):



        #Quadrants
        #north-west node
        nw_node = node(
            self.cx - (self.width * 0.25),
            self.cy + (self.height * 0.25),
            (self.width * 0.5),
            (self.height * 0.5))

        #north-east node
        ne_node = node(
            self.cx + (self.width * 0.25),
            self.cy + (self.height * 0.25),
            (self.width * 0.5),
            (self.height * 0.5))

        #south-west node
        sw_node = node(
            self.cx - (self.width * 0.25),
            self.cy - (self.height * 0.25),
            (self.width * 0.5),
            (self.height * 0.5))

        #south-east node
        se_node = node(
            self.cx + (self.width * 0.25),
            self.cy - (self.height * 0.25),
            (self.width * 0.5),
            (self.height * 0.5))
        
        self.children = [nw_node, ne_node, sw_node, se_node]

    def insert(self, star):
        if (self.contains(star) == False): #If star is not contained within boundary
            return False
        
        if self.n_stars > 0:
            self.createChildren()
            for child in self.children:
                child.insert(self.star)
            self.star = None

        for child in self.children:
            child.add(star)


        else:
            self.child = child

        
            


