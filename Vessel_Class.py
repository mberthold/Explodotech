import threading
import math
import random
import numpy as np


class Vessel:
    # A very simple missile - maybe even the prototype for all missiles.. who knows..
    ID = "None"
    name = "New Ship"
    pos = np.array([0.0, 0.0])
    
    velocity = np.array([0.0, 0.0])
    size = 1.0
    
    isAlive = True



    def __init__ (self, ident, pos, name):
        self.ID = ident
        self.name = name
        self.pos = pos
        

    def getPosition (self):
        return (self.pos)

    def setVelocity(self, vel):
        print ("Setting Speed to    :   ", vel)
        self.velocity = vel
        
        
    # only for debugging purposes
    def stopMoving(self):
        self.velocity = np.array([0.0,0.0])

    def updatePosition(self, dT):
        self.pos = self.velocity * dT + self.pos
        

    def update(self, dT):
        self.updatePosition(dT)



    


