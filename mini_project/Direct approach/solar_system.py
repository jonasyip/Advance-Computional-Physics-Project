import numpy as np

class body:
    def __init__(self, name, mass, radius, x, y, z, vx, vy, vz):
        
        self.name = name            #Name of the body
        self.mass = mass            #Mass of the body   (kg)
        self.radius = radius        #Radius of the body (km)

        self.x = x                  #x position         (km)
        self.y = y                  #y position         (km)
        self.z = z                  #z position         (km)

        self.vx = vx                #x velocity         (km/s)
        self.vy = vy                #y velocity         (km/s)
        self.vz = vz                #z velocity         (km/s)

    def update(self, timestep, acceleration):
        self.ax = acceleration[0]
        self.ay = acceleration[1] 
        self.az = acceleration[2] 

        #v_i_new = v_i + (a_i * t)
        new_vx = self.vx + (self.ax * timestep)
        new_vy = self.vy + (self.ay * timestep)
        new_vz = self.vz + (self.az * timestep)

        #r_i = r_i + (v_i * t)
        new_x = self.x + (new_vx * timestep)
        new_y = self.y + (new_vy * timestep)
        new_z = self.z + (new_vz * timestep)

        #Write new positions
        self.x = new_x
        self.y = new_y
        self.z = new_z

        #Write new velocities
        self.vx = new_vx
        self.vy = new_vy
        self.vz = new_vz

class solarsystem:
    bodycount = 0
    def __init__(self, nbody):
        self.nbody = nbody
        self.bodies = np.zeros(nbody, dtype=object)

    def __repr__(self):
        return f"[]"

    def insert(self, body):
        if self.bodycount < self.nbody:
            self.bodies[self.bodycount] = body
            self.bodycount += 1
        else:
            print("System reached maxmimum, body not added")

    def update(self, timestep):
        G_const = 1
        for body1 in self.bodies:
            count = 0
            a_array = np.zeros(((self.nbody-1), 3))     #Acceleration array (m/s)
            for body2 in self.bodies:
                if (body1 is not body2):
                    r1 = np.array([body1.x, body1.y, body1.z])
                    r2 = np.array([body2.x, body2.y, body2.z])
                    r_diff = r1 - r2
                    a_i = -1*G_const*((body2.mass*r_diff) / np.power(np.absolute(r_diff), 3))
                    a_array[count] = a_i
                    count += 1
            acceleration = np.sum(a_array)
            
            body1.update(timestep, acceleration)

    def display(self, ax):
        for body1 in self.bodies:
            name = body1.name
            x = body1.x
            y = body1.y
            z = body1.z

            ax.scatter(x,y, label=name)



