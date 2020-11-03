import threading
import math

# The idea is that each vessel will manage its own movement in a seperate thread...
# Let's hope this does not overtax the system... ;)
class Vessel:
    # A very simple missile - maybe even the prototype for all missiles.. who knows..
    iD = "None"
    name = "New Ship"
    posX = 0.0
    posY = 0.0

    # Let's assume our vessel can only move in X-direction this should later be change into a vector!
    xSpeed = 0.0 # Units per second
    speedVector = (0.0 , 0.0) # The vector member - not yet used!
    dT = 1 # The time interval by which we calculate the new position.
    isAlive = True



    def __init__ (self, id, posX, posY, name):
        self.ID = id
        self.posX = posX
        self.posY = posY
    
    def getPosition (self):
        return ((self.posX, self.posY))

    def setSpeed(self, newSpeed):
        print ("Setting Speed to    :   ", newSpeed)
        self.xSpeed = newSpeed
        #self.speedVector = newSpeed
        
    # only for debugging purposes
    def stopMoving(self):
        self.xSpeed = 0.0

    def updatePosition(self):
        self.posX = (self.xSpeed * self.dT) + self.posX




