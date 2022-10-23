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

class quadtree:
    def __init__(self, boundary, node_capacity, stars):
        self.boundary = boundary
        self.node_capacity = node_capacity
        self.stars = stars

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
            nw_boundary = square(
                centre_x - (width * 0.25),
                centre_y + (height * 0.25),
                (width * 0.5),
                (height * 0.5))
            self.nw = quadtree(nw_boundary, self.max_capcity, (self.level+1))
            
            #north-east boundary
            ne_boundary = square(
                centre_x + (width * 0.25),
                centre_y + (height * 0.25),
                (width * 0.5),
                (height * 0.5))
            self.ne = quadtree(ne_boundary, self.max_capcity, (self.level+1))

            #south-west boundary
            sw_boundary = square(
                centre_x - (width * 0.25),
                centre_y - (height * 0.25),
                (width * 0.5),
                (height * 0.5))
            self.sw = quadtree(sw_boundary, self.max_capcity, (self.level+1))

            #south-east boundary
            se_boundary = square(
                centre_x + (width * 0.25),
                centre_y - (height * 0.25),
                (width * 0.5),
                (height * 0.5))
            self.se = quadtree(se_boundary, self.max_capcity, (self.level+1))

            # print(self.level, self.stars)
            # print("self.nw.stars %s" % self.nw.stars)
            # print("self.ne.stars %s" % self.ne.stars)
            # print("self.sw.stars %s" % self.sw.stars)
            # print("self.se.stars %s" % self.se.stars)

            self.divided = True

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
                    return True
                elif (self.ne.insert(star) == True):
                    return True
                elif (self.sw.insert(star) == True):
                    return True
                elif (self.se.insert(star) == True):
                    return True
                else:
                    return False


                #Return
                # return(
                # self.nw.insert(star) or
                # self.ne.insert(star) or
                # self.sw.insert(star) or
                # self.se.insert(star)) #Recusion
                # #LINK WITH NODE CLASS?
                    
                # if (self.nw.insert(star) == True):

            
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

        def search(self, boundary, stars_searched):
            """
            
            """
            for star in self.stars:
                if boundary.contains(star):
                    stars_searched.append(star)

            if (self.divided == True): #Recusive
                self.nw.query(boundary, stars_searched)
                self.ne.query(boundary, stars_searched)
                self.se.query(boundary, stars_searched)
                self.sw.query(boundary, stars_searched)
            return stars_searched