import numpy as np
import math
import Vessel_Class

class Ship(Vessel_Class.Vessel):
    """Basic steerable ship"""
    rotation_speed = 0.0                        # degrees per second
    max_rotation_speed = 30.0                   # degrees per second
    orientation_vector = np.array([1.0, 0.0])
    heading = 0.0                              # degrees!

    max_acceleration = 5.0
    curr_acceleration = 0.0
    vessel_type = "ship"

    # debugging only!!!
    direction = 1

    def __init__(self, ident, pos, name):
        super().__init__(ident, pos, name)

    def update(self, dT):
        super().update(dT)
        if self.rotation_speed != 0.0:
            self.rotate(dT, self.rotation_speed)
        if self.curr_acceleration != 0.0:
            self.accelerate(dT)


        ''' This code will cause the ALL ships to oszilate!
        if self.pos[0] < 550 and self.direction == 1 or self.pos[0] < 450:
            self.curr_acceleration = 5.0
        elif self.pos[0] > 550 :
            self.curr_acceleration = - 5.0
        if self.pos[0] > 550:
            self.direction = 0
        elif self.pos[0] < 450:
            self.direction = 1
        '''

    def update_orientation_vector(self):
        x = math.sin(self.heading)
        y = math.cos(self.heading)
        self.orientation_vector = np.array([x,y])

    def update_heading(self):
        pass
        #self.heading = -(np.angle(self.orientation_vector[0] + self.orientation_vector[1]*j) - 90)

    def rotate(self, dT, rotation_speed):
        new_heading = self.heading + rotation_speed*dT
        if new_heading < 0.0:
            new_heading += 360
        elif new_heading > 360:
            new_heading -= 360
        self.heading = new_heading
        self.update_orientation_vector()

    def accelerate(self, dT):
        self.velocity = self.velocity + self.orientation_vector*self.curr_acceleration*dT