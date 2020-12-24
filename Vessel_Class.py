import threading
import math
import random
import numpy as np


class Vessel:
    """Generic Vessel-class"""
    ID = "None"
    name = "New Ship"
    faction = "None"
    vessel_type = "None"
    
    pos = np.array([0.0, 0.0])

    velocity = np.array([0.0, 0.0])
    
    size = 1.0
    visibility = 1.0
    
    isAlive = True

    
    def __init__ (self, ident, pos, name, faction = "None"):
        self.ID = ident
        self.name = name
        self.pos = pos
        self.vessel_type = "generic_ship"
        self.faction = faction
        

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



    


