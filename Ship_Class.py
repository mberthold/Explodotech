import numpy as np
import math
import Vessel_Class

class Ship(Vessel_Class.Vessel):
    """Basic steerable ship"""
    rotation_speed = 0.0                        # degrees per second
    max_rotation_speed = 30.0                   # degrees per second
    heading_vector = np.array([1.0, 0.0])       # where is the nose pointing - as a vector
    heading = 0.0                               # and in degrees!

    max_acceleration = 5.0
    curr_acceleration = 0.0
    vessel_type = "ship"

    # debugging only!!!
    direction = 1

    def __init__(self, ident, pos, name, faction):
        super().__init__(ident, pos, name, faction)
        self.rotate(0, 0)

    def update(self, dT):
        super().update(dT)
        if self.rotation_speed != 0.0:
            self.rotate(dT, self.rotation_speed)
        if self.curr_acceleration != 0.0:
            self.accelerate(dT)

        print("Heading: " + str(self.heading))
        print("Heading vector: " + str(self.heading_vector[0]))
        print("Heading vector: " + str(self.heading_vector[1]))

    def update_heading_vector(self):
        rad_heading = (self.heading/180)*np.pi
        x = math.sin(rad_heading)
        y = math.cos(rad_heading)
        self.heading_vector = np.array([x,y])
        return x, y

    def update_heading(self):
        pass
        #self.heading = -(np.angle(self.heading_vector[0] + self.heading_vector[1]*j) - 90)

    def rotate(self, dT, rotation_speed):
        new_heading = self.heading + rotation_speed*dT
        if new_heading < 0.0:
            new_heading += 360
        elif new_heading > 360:
            new_heading -= 360
        self.heading = new_heading
        self.update_heading_vector()

    def accelerate(self, dT):
        self.velocity = self.velocity + self.heading_vector*self.curr_acceleration*dT

    def set_heading(self, new_heading):
        self.heading = new_heading
        self.update_heading_vector()
        return self.heading